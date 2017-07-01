from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="marcokoch", channel="testing", \
        stable_branch_pattern="^v[0-9]+(\\.[0-9])*-stable$")
    builder.add_common_builds(shared_option_name="libunwind:shared")
    builder.run()
