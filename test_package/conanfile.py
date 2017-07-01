from conans import ConanFile, CMake, tools
import os


package_version = "1.2.1"
channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "marcokoch")


class LibunwindTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libunwind/%s@%s/%s" % (package_version, username, channel)
    generators = "cmake"


    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        
        self.output.info("Configuring test application")
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        
        self.output.info("Building test application")
        cmake.build()


    def test(self):
        if not tools.cross_building(self.settings):
            cmake = CMake(self)            
            self.output.info("Running tests")
            cmake.test()
        else:
            self.output.info("Skipping tests due to cross-build")
