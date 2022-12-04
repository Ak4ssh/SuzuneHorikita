from src import LOAD, NO_LOAD, LOGGER
import sys


def __list_all_source():
    from os.path import dirname, basename, isfile
    import glob

    # This generates a list of source in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_source = [
        basename(f)[:-3]
        for f in mod_paths
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    if LOAD or NO_LOAD:
        to_load = LOAD
        if to_load:
            if not all(
                any(mod == module_name for module_name in all_source)
                for mod in to_load
            ):
                LOGGER.error("Invalid load order names, Quitting...")
                sys.exit(1)

            all_source = sorted(set(all_source) - set(to_load))
            to_load = list(all_source) + to_load

        else:
            to_load = all_source

        if NO_LOAD:
            LOGGER.info("Not loading: {}".format(NO_LOAD))
            return [item for item in to_load if item not in NO_LOAD]

        return to_load

    return all_source


ALL_source = __list_all_source()
LOGGER.info("source to load: %s", str(ALL_source))
__all__ = ALL_source + ["ALL_source"]
