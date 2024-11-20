import os
import sys
from typing import List, Optional, Dict
import functools
import inspect


class Platform:
    def __init__(self):
        self.sys_type = sys.platform

    def get_sys_platform(self):
        return self.sys_type

    @classmethod
    def type_checking(cls, os_type: str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return (
                    func(*args, **kwargs) if cls().get_sys_platform() == os_type else None
                )

            return wrapper

        return decorator


class SearchDataList(Platform):
    def __init__(
            self,
            filename,
            file_suffix: Optional[str] = None,
            file_suffixes: Optional[List:str] = None,
            filenames: Optional[List:str] = None,
    ):
        super().__init__()
        self.filename = filename
        self.file_suffix = file_suffix
        self.file_suffixes = file_suffixes
        self.filenames = filenames

    @classmethod
    def none_validation(cls, argument: str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                inner_instance = args[0]

                init_method = inspect.getattr_static(cls, "__init__", None)
                if init_method is not None:
                    init_params = inspect.signature(init_method).parameters
                    if argument in init_params:
                        param_value = getattr(inner_instance, argument)
                        if param_value is None:
                            raise ValueError(
                                f"The {argument} attribute cannot be None."
                            )
                return func(*args, **kwargs)

            return wrapper

        return decorator


class Search(SearchDataList):
    def __init__(self, filename, file_suffix=None, file_suffixes=None, filenames=None):
        super().__init__(filename, file_suffix, file_suffixes, filenames)

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("filename")
    def filename_lookup(self) -> Dict:
        """
        A simple class method which look for a collection of file by its filename and return the specific path to it.
        """
        routes = {}
        if self.filename[len(self.filename) - 1] != '*':
            for root, dirs, files in os.walk("C://"):
                if self.filename in files:
                    routes[self.filename] = os.path.join(os.path.abspath(root), self.filename) + " :File"
                if self.filename in dirs:
                    routes[self.filename] = os.path.join(os.path.abspath(root), self.filename) + " :Directory"
        else:
            for root, dirs, files in os.walk("C://"):
                # self.filename=self.filename[0:len(self.filename) - 1]
                # For directories
                routes.update(
                    {dir: os.path.join(os.path.abspath(root), dir) + " :Directory"
                     for dir in dirs
                     if dir.__contains__(self.filename[0:len(self.filename) - 1])
                     })
                # For Files
                routes.update(
                    {file: os.path.join(os.path.abspath(root), file) + " :File"
                     for file in files
                     if file.__contains__(self.filename[0:len(self.filename) - 1])
                     })
        if routes:
            return routes
        else:
            return {"message": "Couldn't find a file you mentioned."}

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("filename")
    def is_a_file(self) -> bool:
        """
        Determining whether it is a file or return False
        """
        return os.path.isfile(self.filename)

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("filename")
    def is_a_directory(self) -> bool:
        """
        Determining whether it is a file or return True
        """
        return os.path.isdir(self.filename)

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("file_suffix")
    def suffix_lookup(self) -> Dict:
        """
        Look for files based on suffixes
        """
        routes = {}
        if self.file_suffix[len(self.file_suffix) - 1] != '*':
            for root, dirs, files in os.walk("C://"):
                for file in files:
                    if self.file_suffix == os.path.splitext(file)[1]:
                        routes[file] = os.path.join(os.path.abspath(root), file) + " :File"
        else:
            for root, dirs, files in os.walk("C://"):
                routes.update({file: os.path.join(os.path.abspath(root), file) + " :File"
                               for file in files if os.path.splitext(file)[1].__contains__(
                        self.file_suffix[0:len(self.file_suffix) - 1])})
        if routes:
            return routes
        else:
            return {"message": "Couldn't find a file you mentioned."}

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("filenames")
    def filenames_lookup(self) -> List:
        """
        Look for a collection of files and return a list of them
        """
        result = []
        for file in self.filenames:
            self.filename = file
            result.append(self.filename_lookup())
        if result:
            return result
        else:
            return ["message : Couldn't find a file you mentioned."]

    @Platform.type_checking("win32")
    @SearchDataList.none_validation("file_suffixes")
    def suffixes_lookup(self) -> List:
        """
        Look for a collection of files and return a list of them based on the provided suffixes
        """
        result = []
        for suffix in self.file_suffixes:
            self.file_suffix = suffix
            result.append(self.suffix_lookup())
        if result:
            return result
        else:
            return ["message : Couldn't find a file you mentioned."]


instance = Search(None,file_suffix=".m*")

print(instance.suffix_lookup())
