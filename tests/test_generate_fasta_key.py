import unittest
import os
import sys
import tempfile
from subprocess import call
from filecmp import cmp
import py_compile

class GenerateVariantSequences(unittest.TestCase):
    def setUp(self):
        self.python = sys.executable
        base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
        self.executable_dir = os.path.join(base_dir, 'pvac_seq')
        self.test_data_dir  = os.path.join(base_dir, 'test_data')
        self.sample_name             = 'Test'
        self.peptide_sequence_length = 21

    def tearDown(self):
        del self.executable_dir
        del self.test_data_dir
        del self.sample_name
        del self.peptide_sequence_length

    def test_generate_fasta_key_runs_and_produces_expected_output(self):
        generate_fasta_key_input_file  = os.path.join(self.test_data_dir, ("%s_%s.fa" % (self.sample_name, self.peptide_sequence_length)))
        generate_fasta_key_output_file = tempfile.NamedTemporaryFile().name
        generate_fasta_key_executable  = os.path.join(self.executable_dir, 'generate_fasta_key.py')
        self.assertTrue(py_compile.compile(generate_fasta_key_executable))

        generate_fasta_key_command = "%s %s %s %s" % (self.python, generate_fasta_key_executable, generate_fasta_key_input_file, generate_fasta_key_output_file)

        self.assertFalse(call(generate_fasta_key_command, shell=True))
        expected_output_file = os.path.join(self.test_data_dir, ("%s_%s.key" % (self.sample_name, self.peptide_sequence_length)))
        self.assertTrue(cmp(generate_fasta_key_output_file, expected_output_file, shallow=False))

if __name__ == '__main__':
    unittest.main()

