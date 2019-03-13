"""
This module represents a device.

Computer Systems Architecture Course
Assignment 1
March 2016

Nume: Munteanu Filip
Grupa: 332CB
"""

from threading import Thread, Condition, Lock, Event
from Queue import Queue

class ReusableBarrier(object):
    """ Bariera reentranta, implementata folosind o variabila conditie """

    def __init__(self, num_threads):
        self.num_threads = num_threads
        self.count_threads = self.num_threads
        self.cond = Condition()                  # blocheaza/deblocheaza thread-urile
                                                 # protejeaza modificarea contorului

    def wait(self):
        """ wait for all the threads to reach the barrier """
        self.cond.acquire()                      # intra in regiunea critica
        self.count_threads -= 1
        if self.count_threads == 0:
            self.cond.notify_all()               # deblocheaza toate thread-urile
            self.count_threads = self.num_threads
        else:
            self.cond.wait()
        self.cond.release()                     # iese din regiunea critica


class Device(object):
    """
    Class that represents a device.
    """

    def __init__(self, device_id, sensor_data, supervisor):
        """
        Constructor.

        @type device_id: Integer
        @param device_id: the unique id of this node; between 0 and N-1

        @type sensor_data: List of (Integer, Float)
        @param sensor_data: a list containing (location, data) as measured by this device

        @type supervisor: Supervisor
        @param supervisor: the testing infrastructure's control and validation component
        """
        self.device_id = device_id
        self.sensor_data = sensor_data
        self.supervisor = supervisor
        self.scripts = []
        self.timepoint_done = Event()
        self.thread = DeviceThread(self)
        self.thread.start()
        self.location_locks = {}
        self.barrier = None

    def __str__(self):
        """
        Pretty prints this device.

        @rtype: String
        @return: a string containing the id of this device
        """
        return "Device %d" % self.device_id

    def setup_devices(self, devices):
        """
        Setup the devices before simulation begins.
        Device 0 will create a barrier and a list of locks for locations
        and it will share them with the other devices

        @type devices: List of Device
        @param devices: list containing all devices
        """

        if self.device_id == 0:
            self.barrier = ReusableBarrier(len(devices))
            for dev in devices:
                dev.barrier = self.barrier
                dev.location_locks = self.location_locks
                for location in dev.sensor_data:
                    if not self.location_locks.has_key(location):
                        self.location_locks[location] = Lock()

    def assign_script(self, script, location):
        """
        Provide a script for the device to execute.

        @type script: Script
        @param script: the script to execute from now on at each timepoint; None if the
            current timepoint has ended

        @type location: Integer
        @param location: the location for which the script is interested in
        """
        if script is not None:
            self.scripts.append((script, location))
        else:
            self.timepoint_done.set()

    def get_data(self, location):
        """
        Returns the pollution value this device has for the given location.

        @type location: Integer
        @param location: a location for which obtain the data

        @rtype: Float
        @return: the pollution value
        """
        return self.sensor_data[location] if location in self.sensor_data else None

    def set_data(self, location, data):
        """
        Sets the pollution value stored by this device for the given location.

        @type location: Integer
        @param location: a location for which to set the data

        @type data: Float
        @param data: the pollution value
        """
        if location in self.sensor_data:
            self.sensor_data[location] = data

    def shutdown(self):
        """
        Instructs the device to shutdown (terminate all threads). This method
        is invoked by the tester. This method must block until all the threads
        started by this device terminate.
        """
        self.thread.join()


class DeviceThread(Thread):
    """
    Class that implements the device's worker thread.
    """

    def __init__(self, device):
        """
        Constructor.

        @type device: Device
        @param device: the device which owns this thread

        Queue "q" is used to store the scripts to be run by workers
        There are 8 threads used to execute the scripts
        """
        Thread.__init__(self, name="Device Thread %d" % device.device_id)
        self.device = device
        self.neighbours = None
        self.queue = Queue()
        self.threads = []
        for _ in xrange(8):
            thread = Thread(target=worker, args=(self,))
            self.threads.append(thread)

    def run(self):

        # starting workers
        for thread in self.threads:
            thread.start()

        while True:

            # get the current neighbourhood
            self.neighbours = self.device.supervisor.get_neighbours()
            if self.neighbours is None:
                break

            self.device.timepoint_done.wait()

            # add scripts to queue
            for (script, location) in self.device.scripts:
                self.queue.put((script, location))

            # wait for the workers to finish executing all scripts
            self.queue.join()

            self.device.timepoint_done.clear()
            # synchronise the devices
            self.device.barrier.wait()

        # close the threads
        for _ in xrange(8):
            self.queue.put((-1, -1))
        for thread in self.threads:
            thread.join()

def worker(dev_thread):
    """ This function is used to run scripts from the queue """

    while True:
        # Get a script from the queue and execute it
        script, location = dev_thread.queue.get()

        # If location and script are -1 it means that the thred should close
        if location == -1 and script == -1:
            break

        # The reading, processing and writing are made atomic with a lock on location
        dev_thread.device.location_locks[location].acquire()

        script_data = []
        # collect data from current neighbours
        for device in dev_thread.neighbours:
            data = device.get_data(location)
            if data is not None:
                script_data.append(data)
        # add our data, if any
        data = dev_thread.device.get_data(location)
        if data is not None:
            script_data.append(data)

        if script_data != []:
            # run script on data
            result = script.run(script_data)

            # update data of neighbours, hope no one is updating at the same time
            for device in dev_thread.neighbours:
                device.set_data(location, result)
            # update our data, hope no one is updating at the same time
            dev_thread.device.set_data(location, result)

        dev_thread.device.location_locks[location].release()

        dev_thread.queue.task_done()
