import unittest
import boris_analysis.dialogs as dialogs


class TestNormalization(unittest.TestCase):

    def test_normalize_speech_act_name(self):
        test_set = ["bye", "explConfirm", "indicateValues", "indicateValues1", "indicateValues2", "inform",
                 "informAndOfferMore", "offerModification", "offerRefinement", "repetitionRequest", "request",
                 "Bye", "ExplicitConfirmation", "IndicateValue", "IndicateValuesOne", "Inform", "InformAndOfferMore",
                 "OfferModification", "OfferRefinement", "RepetitionRequest", "Request", "Accept",
                 "EMPTY", "HangUp", "Inform", "Negate", "Provide", "accept", "accept provide", "affirm",
                 "affirm provide", "negate", "neglect", "provide", ""]

        normalized = list(map(lambda i: dialogs.normalize_speech_act_name(i), test_set))

        self.assertEqual(len(test_set), len(normalized))

    def test_normalize_field_values(self):
        test_value = "foodtype time price localization "
        expected_result = "foodtype localization price time"

        normalized_value = dialogs.normalize_field_values(test_value)

        self.assertEqual(expected_result, normalized_value)
