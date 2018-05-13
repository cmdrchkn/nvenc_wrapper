import sys
import os
import argparse
from subprocess import check_call, CalledProcessError

# -- Globals -- #
__OUTPUT_ROOT = r"D:\BD\conv"
__NVENC_PATH = r"C:\tools\nvenc\NVEncC64.exe"
__NVENV_OPTS_CQP = [
    '--cqp', '22',
]
__NVENC_OPTS_COMMON = [
    '--chapter-copy', 
    '--sub-copy',
    '--audio-stream', '5.1,:stereo',
    '--audio-codec', 'aac',
    '--audio-bitrate', '224',
]
__NVENC_OPTS_1080 = [
    '-c', 'hevc',
    '--output-res', '1920x1080',
]
__NVENC_OPTS_720 = [
    '-c', 'h264',
    '--output-res', '1280x720',
]


# -- Functions -- #
def usage():
    print()
    print(os.path.split(sys.argv[0])[1], 'full\\path\\to\\input.file')
    print('  Use NVEnc to generate an HEVC-encoded file in', __OUTPUT_ROOT)
    print('\n-- Default NVEnc Options (1080p:')
    print('  ' + '\n  '.join(__NVENC_OPTS_1080 + __NVENC_OPTS_COMMON))
    print()
    return

def parse_args():
    parser = argparse.ArgumentParser(
        description='Use NVEnc to generate two files (HEVC@1080p, h264@720p)'
    )
    parser.add_argument(
        'input_file',
        help='source file to re-encode',
        type=str
    )
    parser.add_argument(
        '-nvenc',
        nargs=1,
        metavar='nvenc.exe',
        default=[__NVENC_PATH],
        help='full path to NVEncC64.exe',
        type=str
    )
    parser.add_argument(
        '-o',
        nargs=1,
        metavar='output_root',
        default=[__OUTPUT_ROOT], 
        help='directory to write the new files',
        type=str
    )
    parser.add_argument(
        '-cqp', '-q',
        nargs=1,
        metavar='quality_int',
        default=['22'], 
        help='constant quality setting',
        type=str
    )
    parser.add_argument(
        '-only1080', '-1080',
        default=False, 
        help='only output the hevc@1080p version',
        action="store_true"
    )
    parser.add_argument(
        '-only720', '-720',
        default=False, 
        help='only output the h264@720p version',
        action="store_true"
    )
    parser.add_argument(
        '-overwrite', '-ovr',
        default=False, 
        help='write the output file even if it already exists',
        action="store_true"
    )

    args = parser.parse_args()
    if args.nvenc:
        globals().update({ '__NVENC_PATH': args.nvenc[0] })
        print(' -- Using NVEnc:', __NVENC_PATH)
    if args.o:
        globals().update({ '__OUTPUT_ROOT': args.o[0] })
        print(' -- Using Output Root:', __OUTPUT_ROOT)
    if args.cqp:
        globals().update({ '__NVENV_OPTS_CQP': ['--cqp', args.cqp[0]] })
        print(' -- Using Quality:', __NVENV_OPTS_CQP[1])
    if args.only1080:
        print(' -- Only rendering hevc@1080p')
    if args.only720:
        print(' -- Only rendering h264@720p')
    if args.overwrite:
        print(' -- Will overwrite output files')
    
    return args
    

def encode_me(
        input_path, 
        res="1080",
        nvenc_path=__NVENC_PATH,
        nvenc_opts_1080=__NVENC_OPTS_1080,
        nvenc_opts_720=__NVENC_OPTS_720,
        nvenc_opts_cqp=__NVENV_OPTS_CQP,
        nvenc_opts_common=__NVENC_OPTS_COMMON,
        output_root=__OUTPUT_ROOT
    ):

    if res == '1080':
        options = nvenc_opts_1080 + nvenc_opts_cqp + nvenc_opts_common
    elif res == '720':
        options = nvenc_opts_720 + nvenc_opts_cqp + nvenc_opts_common
    else:
        print('Unknown Resolution passed:', res)
        return

    try:
        output_path = os.path.join(
            output_root,
            os.path.splitext(os.path.split(input_path)[1])[0] + '.' + res + '.mkv'
        )

        print('\n--- Encoding', input_path, '-->', output_path)
        if os.path.exists and not args.overwrite:
            print('  - The file already exists, skipping render')
            return

        cmd = [nvenc_path] + options[:] + [
            '-i', input_path,
            '-o', output_path
        ]
        check_call(cmd)
    except CalledProcessError as e:
        print('Failed to encode', input_path)
        print('Command used: {{', cmd, '}}', sep='')
        print('Exception was', e)
    except FileNotFoundError as e:
        print(cmd)
        print(e)
    return


def main(args):
    if not args.only720:
        encode_me(args.input_file, res='1080')

    if not args.only1080:
        encode_me(args.input_file, res='720')

    return


# -- Run Main -- #
if __name__ == '__main__':
    args = parse_args()
    main(args)
