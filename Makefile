# Starting with unit test host build configuration

BUILD_ROOT_DIR = make_build

# ------------------------------------------------------
# Test runner generator definitions

TEST_RUNNER_GENERATOR = test_harness\Unity\scripts\makeTestRunner.py
UNIT_TEST_RUNNER_SOURCE = tests\_all_tests.c

# ------------------------------------------------------
# Unit tests host build config

UNIT_TESTS_HOST_BUILD_DIR = $(BUILD_ROOT_DIR)\UnitTests_host
UNIT_TESTS_HOST_OBJ_DIR = $(UNIT_TESTS_HOST_BUILD_DIR)\obj
UNIT_TESTS_HOST_CC = gcc
UNIT_TESTS_HOST_DEFINES = -DTARGET_HOST
UNIT_TESTS_HOST_LDFLAGS =
UNIT_TESTS_HOST_INCDIRS = \
    -Iarduino_core\include \
    -Iarduino_core\variants\arduino_due_x \
    -Idevice_libs\CMSIS\CMSIS\Include \
    -Idevice_libs\CMSIS\Device\ATMEL \
    -Idevice_libs\libsam \
    -Isrc \
    -Imy_static_lib \
    -Itest_harness\Unity
UNIT_TESTS_HOST_CFLAGS = $(UNIT_TESTS_HOST_DEFINES) $(UNIT_TESTS_HOST_INCDIRS) -O0 -g3 -Wall

UNIT_TESTS_HOST_TEST_SOURCE = \
    tests\TestProductionCode.c \
    tests\TestProductionCode2.c \
    tests\_all_tests_main.c

UNIT_TESTS_HOST_SOURCES = \
    my_static_lib\my_static_lib_s1.c \
    src\ProductionCode.c \
    src\ProductionCode2.c \
    test_harness\Unity\unity.c \
    test_harness\Unity\unity_fixture.c \
    $(UNIT_TEST_RUNNER_SOURCE) \
    $(UNIT_TESTS_HOST_TEST_SOURCE)

# addprefix is specific to GNU make (?)
UNIT_TESTS_HOST_OBJECTS = $(addprefix $(UNIT_TESTS_HOST_OBJ_DIR)\,$(UNIT_TESTS_HOST_SOURCES:.c=.o))
UNIT_TESTS_HOST_DEPENDS = $(addprefix $(UNIT_TESTS_HOST_OBJ_DIR)\,$(UNIT_TESTS_HOST_SOURCES:.c=.d))

UNIT_TESTS_HOST_EXECUTABLE=ArduinoDue_blank-UnitTestHost.exe


# ------------------------------------------------------
# Unit tests host build config variant

UNIT_TESTS_HOST_VARIANT_BUILD_DIR = $(BUILD_ROOT_DIR)\UnitTests_host_variant
UNIT_TESTS_HOST_VARIANT_OBJ_DIR = $(UNIT_TESTS_HOST_VARIANT_BUILD_DIR)\obj
UNIT_TESTS_HOST_VARIANT_CC = gcc
UNIT_TESTS_HOST_VARIANT_DEFINES = -DTARGET_HOST -DUNIT_TEST_VARIANT1
UNIT_TESTS_HOST_VARIANT_LDFLAGS =
UNIT_TESTS_HOST_VARIANT_INCDIRS = \
    -Iarduino_core\include \
    -Iarduino_core\variants\arduino_due_x \
    -Idevice_libs\CMSIS\CMSIS\Include \
    -Idevice_libs\CMSIS\Device\ATMEL \
    -Idevice_libs\libsam \
    -Isrc \
    -Imy_static_lib \
    -Itest_harness\Unity
UNIT_TESTS_HOST_VARIANT_CFLAGS = $(UNIT_TESTS_HOST_VARIANT_DEFINES) $(UNIT_TESTS_HOST_VARIANT_INCDIRS) -O0 -g3 -Wall

UNIT_TESTS_HOST_VARIANT_TEST_SOURCE = \
    tests\TestProductionCode.c \
    tests\TestProductionCode2.c \
    tests\_all_tests_main.c

UNIT_TESTS_HOST_VARIANT_SOURCES = \
    my_static_lib\my_static_lib_s1.c \
    src\ProductionCode.c \
    src\ProductionCode2.c \
    test_harness\Unity\unity.c \
    test_harness\Unity\unity_fixture.c \
    $(UNIT_TEST_RUNNER_SOURCE) \
    $(UNIT_TESTS_HOST_VARIANT_TEST_SOURCE)

# addprefix is specific to GNU make (?)
UNIT_TESTS_HOST_VARIANT_OBJECTS = $(addprefix $(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\,$(UNIT_TESTS_HOST_VARIANT_SOURCES:.c=.o))
UNIT_TESTS_HOST_VARIANT_DEPENDS = $(addprefix $(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\,$(UNIT_TESTS_HOST_VARIANT_SOURCES:.c=.d))

UNIT_TESTS_HOST_VARIANT_EXECUTABLE=ArduinoDue_blank-UnitTestHost_variant.exe

# ------------------------------------------------------
# Rules


all: $(UNIT_TESTS_HOST_EXECUTABLE) $(UNIT_TESTS_HOST_VARIANT_EXECUTABLE)
	echo "all"

# ----------------------------
# Test runner generator rules

$(UNIT_TEST_RUNNER_SOURCE): $(TEST_SOURCE)
	echo "generating tests"
	python $(TEST_RUNNER_GENERATOR) tests -o $(UNIT_TEST_RUNNER_SOURCE)

# ----------------------------
# Unit tests host build rules

$(UNIT_TESTS_HOST_EXECUTABLE): $(UNIT_TESTS_HOST_OBJECTS)
	echo "exe"
	$(UNIT_TESTS_HOST_CC) $(UNIT_TESTS_HOST_LDFLAGS) -o $(UNIT_TESTS_HOST_BUILD_DIR)\$@ $(UNIT_TESTS_HOST_OBJECTS) -lm -lgcc

$(UNIT_TESTS_HOST_OBJECTS): $(UNIT_TESTS_HOST_OBJ_DIR)\\%.o: %.c $(UNIT_TESTS_HOST_OBJ_DIR)\dummy.txt
	$(UNIT_TESTS_HOST_CC) $(UNIT_TESTS_HOST_CFLAGS) -c $< -o $@

$(UNIT_TESTS_HOST_OBJ_DIR)\dummy.txt:
	python make_helpers\create_build_dirs.py $(UNIT_TESTS_HOST_OBJECTS)
	echo "" > $(UNIT_TESTS_HOST_OBJ_DIR)\dummy.txt

# ----------------------------
# Unit tests host variant build rules

$(UNIT_TESTS_HOST_VARIANT_EXECUTABLE): $(UNIT_TESTS_HOST_VARIANT_OBJECTS)
	echo "exe"
	$(UNIT_TESTS_HOST_VARIANT_CC) $(UNIT_TESTS_HOST_VARIANT_LDFLAGS) -o $(UNIT_TESTS_HOST_VARIANT_BUILD_DIR)\$@ $(UNIT_TESTS_HOST_VARIANT_OBJECTS) -lm -lgcc

$(UNIT_TESTS_HOST_VARIANT_OBJECTS): $(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\\%.o: %.c $(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\dummy.txt
	$(UNIT_TESTS_HOST_VARIANT_CC) $(UNIT_TESTS_HOST_VARIANT_CFLAGS) -c $< -o $@

$(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\dummy.txt:
	python make_helpers\create_build_dirs.py $(UNIT_TESTS_HOST_VARIANT_OBJECTS)
	echo "" > $(UNIT_TESTS_HOST_VARIANT_OBJ_DIR)\dummy.txt

clean:
	del $(UNIT_TEST_RUNNER_SOURCE)
	rmdir /S /Q $(BUILD_ROOT_DIR)