#include "unity.h"
#include "unity_fixture.h"

TEST_GROUP_RUNNER(ProductionCode)
{
  RUN_TEST_CASE(ProductionCode, FindFunction_WhichIsBroken_ShouldReturnZeroIfItemIsNotInList_WhichWorksEvenInOurBrokenCode);
  RUN_TEST_CASE(ProductionCode, FindFunction_WhichIsBroken_ShouldReturnTheIndexForItemsInList_WhichWillFailBecauseOurFunctionUnderTestIsBroken);
  RUN_TEST_CASE(ProductionCode, FunctionWhichReturnsLocalVariable_ShouldReturnTheCurrentCounterValue);
  RUN_TEST_CASE(ProductionCode, FunctionWhichReturnsLocalVariable_ShouldReturnTheCurrentCounterValueAgain);
  RUN_TEST_CASE(ProductionCode, FunctionWhichReturnsLocalVariable_ShouldReturnCurrentCounter_ButFailsBecauseThisTestIsActuallyFlawed);
}

TEST_GROUP_RUNNER(ProductionCode2)
{
  RUN_TEST_CASE(ProductionCode2, IgnoredTest);
  RUN_TEST_CASE(ProductionCode2, AnotherIgnoredTest);
  RUN_TEST_CASE(ProductionCode2, ThisFunctionHasNotBeenTested_NeedsToBeImplemented);
}

void RunAllTests(void)
{
    RUN_TEST_GROUP(ProductionCode);
    RUN_TEST_GROUP(ProductionCode2);
}
