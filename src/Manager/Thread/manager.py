from threading import Thread
from typing import Any, Callable, Optional, Union
from datetime import datetime
from enum import Enum

class ThreadStatus(Enum):
    Created = 0
    Actived = 1
    Sleeping = 2

class ThreadManaged(Thread):

    def __init__(self, runnable: Callable, manager: 'ThreadManager', name: Optional[str] = None) -> None:
        self.manager: ThreadManager = manager
        self.__runnable__: Callable = runnable
        self.__args__: list = ()
        self.__kwargs__: dict = {}

        if name == None: self.name: str = "ThreadManaged-" + str(len(manager.__threads__))
        else: self.name: str = name

        self.created_on: float = datetime.now().timestamp()
        self.started_on: float = 0
        self.status: ThreadStatus = ThreadStatus.Created

        super().__init__(name=self.name)

    def run(self) -> None:
        self.started_on: float = datetime.now().timestamp()
        self.status: ThreadStatus = ThreadStatus.Actived
        self.__runnable__(*self.__args__, **self.__kwargs__)
        self.status: ThreadStatus = ThreadStatus.Sleeping

    def start(self, *args, **kwargs) -> None:
        self.__args__: list = args
        self.__kwargs__: dict = kwargs

        super().start()


class ThreadManager:

    def __init__(self) -> None:
        self.__memory__: dict[str, Any] = dict[str, Any]
        self.__threads__: list[ThreadManaged] = list[ThreadManaged]

    def set_memory(self, name: str, value) -> None:
        self.__memory__[name] = value

    def get_memory(self, name: str):
        return self.__memory__[name]

    def del_memory(self, name: str) -> None:
        del self.__memory__[name]

    def create_thread(self, runnable: Callable, name: Optional[str] = None) -> None:
        self.__threads__.append(ThreadManaged(runnable=runnable, manager=self, name=name))

    def del_thread(self, name: Union[str, int]) -> None:
        if isinstance(name, int): del self.__threads__[name]
        else:
            for thread in self.__threads__:
                if thread.name == name: self.__threads__.remove(thread)

    def start_thread(self, name: Union[str, int], *args, **kwargs) -> None:
        if isinstance(name, int): self.__threads__[name].start(args=args, kwargs=kwargs)
        else:
            for thread in self.__threads__:
                if thread.name == name: thread.start(args=args, kwargs=kwargs)

    def get_thread(self, name: Union[str, int]) -> ThreadManaged:
        if isinstance(name, int): return self.__threads__[name]
        else:
            for thread in self.__threads__:
                if thread.name == name: return thread

    def get_all_created(self, relative_time: int = None) -> list[ThreadManaged]:
        if relative_time == None:
            result = []
            for thread in self.__threads__:
                if thread.status == ThreadStatus.Created: result.append(thread)
            return result
        else:
            result = []
            for thread in self.__threads__:
                if thread.status == ThreadStatus.Created:
                    if datetime.now().timestamp() - thread.created_on >= relative_time: result.append(thread)
            return result

    def get_all_actived(self) -> list[ThreadManaged]:
        result = []
        for thread in self.__threads__:
            if thread.status == ThreadStatus.Actived: result.append(thread)
        return result

    def get_all_sleeping(self, relative_time: int = None) -> list[ThreadManaged]:
        if relative_time == None:
            result = []
            for thread in self.__threads__:
                if thread.status == ThreadStatus.Sleeping: result.append(thread)
            return result
        else:
            result = []
            for thread in self.__threads__:
                if thread.status == ThreadStatus.Sleeping:
                    if datetime.now().timestamp() - thread.created_on >= relative_time: result.append(thread)
            return result