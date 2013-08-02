# Starting with unit test host build configuration

# ------------------------------------------------------
# Build config

BUILD_DIR = make_build
OBJ_DIR = $(BUILD_DIR)\obj
CC = gcc
DEFINES = -DTARGET_HOST
LDFLAGS =
INCDIRS = \
    -Iarduino_core\include \
    -Iarduino_core\variants\arduino_due_x \
    -Idevice_libs\CMSIS\CMSIS\Include \
    -Idevice_libs\CMSIS\Device\ATMEL \
    -Idevice_libs\libsam \
    -Isrc \
    -Imy_static_lib \
    -Itest_harness\Unity
CFLAGS = $(DEFINES) $(INCDIRS) -O0 -g3 -Wall

TEST_RUNNER_GENERATOR = test_harness\Unity\scripts\makeTestRunner.py
UNIT_TEST_RUNNER_SOURCE = tests\_all_tests.c

TEST_SOURCE = \
    tests\TestProductionCode.c \
    tests\TestProductionCode2.c \
    tests\_all_tests_main.c

SOURCES = \
    my_static_lib\my_static_lib_s1.c \
    src\ProductionCode.c \
    src\ProductionCode2.c \
    test_harness\Unity\unity.c \
    test_harness\Unity\unity_fixture.c \
    $(UNIT_TEST_RUNNER_SOURCE) \
    $(TEST_SOURCE)

# addprefix is specific to GNU make
OBJECTS = $(addprefix $(OBJ_DIR)\,$(SOURCES:.c=.o))
DEPENDS = $(addprefix $(OBJ_DIR)\,$(SOURCES:.c=.d))

# OBJECTS = \
    # $(OBJ_DIR)\TestProductionCode.o \
    # $(OBJ_DIR)\TestProductionCode2.o \
    # $(OBJ_DIR)\_all_tests_main.o \
    # $(OBJ_DIR)\my_static_lib_s1.o \
    # $(OBJ_DIR)\ProductionCode.o \
    # $(OBJ_DIR)\ProductionCode2.o \
    # $(OBJ_DIR)\unity.o \
    # $(OBJ_DIR)\unity_fixture.o \
    # $(OBJ_DIR)\_all_tests.o

EXECUTABLE=ArduinoDue_blank-UnitTestHost.exe

# ------------------------------------------------------
# Rules

all: $(EXECUTABLE)
	echo "all"

$(EXECUTABLE): $(OBJECTS)
	echo "exe"
	$(CC) $(LDFLAGS) -o $(BUILD_DIR)\$@ $(OBJECTS) -lm -lgcc

$(UNIT_TEST_RUNNER_SOURCE): $(TEST_SOURCE)
	echo "generating tests"
	python $(TEST_RUNNER_GENERATOR) tests -o $(UNIT_TEST_RUNNER_SOURCE)

# FIXME:
# According to this:
# http://stackoverflow.com/questions/13552575/gnu-make-pattern-to-build-output-in-different-directory-than-src
# the following rule should work:
#
$(OBJECTS): $(OBJ_DIR)\\%.o: %.c $(OBJ_DIR)\dummy.txt
	$(CC) $(CFLAGS) -c $< -o $@
#
# however make produces an error: "doesn't match the target pattern"


$(OBJ_DIR)\dummy.txt:
	python make_helpers\create_build_dirs.py $(OBJECTS)
	echo "" > $(OBJ_DIR)\dummy.txt

clean:
	del $(UNIT_TEST_RUNNER_SOURCE)
	rmdir /S /Q $(BUILD_DIR)