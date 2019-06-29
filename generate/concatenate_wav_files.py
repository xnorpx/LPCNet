from typing import List, AnyStr
import logging
import sys
import os


def concatenate_wav_files(wav_file_list: List, output_pcm_file: AnyStr) -> None:
    if len(wav_file_list) < 2:
        logging.info(
            'wav_file_list needs at least 2 wav_files to concatenate, wav_file_list: {}'.format(wav_file_list))
        return

    concatenated_pcm = bytearray()
    ref_wave_file = wav_file_list[0]  # will use this as reference format to compare to the rest of the wavfiles

    with open(ref_wave_file, 'rb') as f:
        f.seek(8)
        ref_header = bytearray(f.read(28))
        ref_data = bytearray(f.read())
        data_index = len(ref_data) - ref_data[::-1].find(b'atad') + 4
        concatenated_pcm.extend(ref_data[data_index:])

    channels = int.from_bytes(ref_header[12:14], 'little')
    if channels != 1:
        logging.error(
            "wav file {} has #{} channels, currently script only supports 1 channel".format(ref_wave_file, channels))
    fs = int.from_bytes(ref_header[16:20], 'little')
    if fs not in [8000, 16000, 24000, 32000, 44100, 48000]:
        logging.error(
            "wav file {} has #{} sampling rate, which is not supported".format(ref_wave_file, fs))

    bits_per_sample = int.from_bytes(ref_header[26:28], 'little')
    if bits_per_sample not in [16, 24, 32]:
        logging.error(
            "wav file {} has #{} bits per sample, which is not supported".format(ref_wave_file, bits_per_sample))

    for wav_file in wav_file_list[1:len(wav_file_list)]:
        with open(wav_file, 'rb') as f:
            f.seek(8)
            current_header = bytearray(f.read(28))
            if current_header != ref_header:
                print(ref_header)
                print(current_header)
                logging.error(
                    'abort concatenate of wavefiles as wavfile: {} wav header does not match wavfile {} header'.format(
                        wav_file,
                        wav_file_list[0]))
                return

            ref_data = bytearray(f.read())
            data_index = len(ref_data) - ref_data[::-1].find(b'atad') + 4  # with large files this is gonna be slow
            concatenated_pcm.extend(ref_data[data_index:])

    with open(output_pcm_file, 'wb') as f:
        f.write(concatenated_pcm)

    concatenated_bytes = len(concatenated_pcm)
    concatenated_samples = int(concatenated_bytes // (bits_per_sample / 8))
    concatenated_time_min = int(concatenated_samples // fs) // 60
    logging.info(
        "Concatenated #{} wav files into: {} pcm file with total length {} [min] with samplingrate {} [Hz]".format(
            len(wav_file_list), output_pcm_file, concatenated_time_min, fs))


def find_wav_files(path: AnyStr) -> List:
    wav_files = []
    logging.info("Look for wavfiles in {}".format(path))
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    logging.info("Found {} wavfiles in {}".format(len(wav_files), path))
    return wav_files


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Concatenate wavfiles, assume same format')
    parser.add_argument('wav_file_path', type=str, default=None, help='path to wav files')
    parser.add_argument('output_file', type=str, default=None, help='path to concatenated file')
    parser.add_argument('--log-level', dest='log_level', default='info', help='logging level',
                        choices=['debug', 'info', 'warning', 'error', 'critical'], required=False)

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(pathname)s,%(lineno)d] %(message)s',
                        level=getattr(logging, args.log_level.upper()),
                        stream=sys.stdout)

    logging.info("Start concatenate wav files")
    concatenate_wav_files(find_wav_files(args.wav_file_path), args.output_file)
    logging.info("Stop concatenate wav files")


if __name__ == '__main__':
    main()
