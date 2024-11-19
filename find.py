import os
import sys
from typing import List, Optional
import functools
import inspect
import glob


class Platform:
    def __init__(self):
        self.sys_type = sys.platform

    def get_sys_platform(self):
        return self.sys_type

    @classmethod
    def type_checking(cls, type: str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return (
                    func(*args, **kwargs) if cls().get_sys_platform() == type else None
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
                instance = args[0]

                init_method = inspect.getattr_static(cls, "__init__", None)
                if init_method is not None:
                    init_params = inspect.signature(init_method).parameters
                    if argument in init_params:
                        param_value = getattr(instance, argument)
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

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("filename")
    def filename_lookup(self) -> List:
        """
        A simple classmethod which look for a collection of file by its filename and return the specific path to it.
        """
        looked_up_files = []
        for root, dirs, files in os.walk("/home"):
            if self.filename in files:
                looked_up_files.append(
                    os.path.join(os.path.abspath(root), self.filename)
                )
            if self.filename in dirs:
                looked_up_files.append(
                    os.path.join(os.path.abspath(root), self.filename)
                )
        if looked_up_files:
            return looked_up_files
        else:
            return {"message": "Couldn't find a file you mentioned."}

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("filename")
    def is_a_file(self) -> bool:
        """
        Determining whethere it is a file or return False
        """
        return os.path.isfile(self.filename)

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("filename")
    def is_a_directory(self) -> bool:
        """
        Determining whethere it is a file or return True
        """
        return os.path.isdir(self.filename)

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("file_suffix")
    def suffix_lookup(self) -> list:
        """
        Look for files based on suffixes
        """
        looked_up_files = []
        for root, dirs, files in os.walk("/home"):
            for file in files:
                if self.file_suffix == os.path.splitext(file)[1]:
                    looked_up_files.append(os.path.join(os.path.abspath(root), file))
        if looked_up_files:
            return looked_up_files
        else:
            return {"message": "Couldn't find a file you mentioned."}

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("filenames")
    def filenames_lookup(self) -> list:
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
            return {"message": "Couldn't find a file you mentioned."}

    @Platform.type_checking("linux")
    @SearchDataList.none_validation("file_suffixes")
    def suffixes_lookup(self) -> list:
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
            return {"message": "Couldn't find a file you mentioned."}


instance = Search(None, file_suffixes=[".mp3", ".mp4"])


print(instance.suffixes_lookup())
