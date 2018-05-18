import sys
import os
import argparse
from subprocess import check_call, CalledProcessError


# -- Classes -- #
class RenderJob():
    def __init__(self, input_file,
        output_root=r"D:\BD\conv",
        encoder_path=r"C:\tools\nvenc\NVEncC64.exe",
        cqp='22',
        output_res='1920x1080',
        codec='hevc'
     ):
        self.output_root = output_root
        self.output_path = None
        self.input_path = input_file
        self.output_res = output_res
        self.encoder_path = encoder_path
        self.codec = codec
        self.cqp = cqp
        self.encoder_options = [
                '-c', self.codec,
                '--output-res', self.output_res,
                '--cqp', self.cqp,
                '--chapter-copy', 
                '--sub-copy',
                '--audio-stream', '5.1,:stereo',
                '--audio-codec', 'aac',
                '--audio-bitrate', '224',
        ]

    def render(self):
        if not self.output_path:
            self.calc_output_path()

        cmd = [self.encoder_path] + self.encoder_options + [
            '-i', self.input_path,
            '-o', self.output_path
        ]
        
        print('\n\n--- Encoding', self.input_path, '-->', self.output_path)
        
        if os.path.exists(self.output_path) and not args.overwrite:
            print('  - The file already exists, skipping render')
            return
            
        try:
            check_call(cmd)
        except CalledProcessError as e:
            print('Failed to encode', self.input_path)
            print('Command used: {{', cmd, '}}', sep='')
            print('Exception was', e)
        except FileNotFoundError as e:
            print(cmd)
            print(e)
        
    def calc_output_path(self):
        self.output_path = os.path.join(
            self.output_root,
            os.path.splitext(
                os.path.split(self.input_path)[1])[0] +
                '.' + self.codec + 
                '.' + self.output_res.split('x')[1] +
                '.mkv'
        )


# -- Functions -- #
def parse_args():
    parser = argparse.ArgumentParser(
        description='Use NVEnc to generate two files (hevc@1080p, h264@720p)'
    )
    parser.add_argument(
        'input_file',
        help='Required; source file to re-encode',
        type=str
    )
    parser.add_argument(
        '-nvenc',
        nargs=1,
        metavar='nvenc.exe',
        default=[r"C:\tools\nvenc\NVEncC64.exe"],
        help='full path to NVEncC64.exe',
        type=str
    )
    parser.add_argument(
        '-o',
        nargs=1,
        metavar='output_root',
        default=[r"D:\BD\conv"], 
        help='directory to write the new files',
        type=str
    )
    parser.add_argument(
        '-cqp',
        nargs=1,
        metavar='quality',
        default=['22'], 
        help='constant quality setting (lower is better)',
        type=str
    )
    parser.add_argument(
        '--overwrite',
        default=False, 
        help='clobber the output file if it already exists',
        action="store_true"
    )
    parser.add_argument(
        '-render',
        default=None,
        metavar=('codec', 'WxH'),
        help='Multi; custom render job e.g. "h264 1280x720"',
        action='append',
        nargs=2,
        type=str,
    )

    args = parser.parse_args()
    if not args.render:
        args.render = [    
            ['hevc', '1920x1080'],
            ['h264', '1280x720']
        ]
    pretty_print_options(args)    
    return args


def pretty_print_single(label, value):
    print(' -- {:<12}  :  {}'.format(label, value))
    return


def pretty_print_pair(label, value1, value2):
    if label == '':
        print('    {:<12}  :  {}@{}'.format(label, value1, value2))
    else:
        print(' -- {:<12}  :  {}@{}'.format(label, value1, value2))
    return


def pretty_print_options(args):
    pretty_print_single('NVEnc', args.nvenc[0])
    pretty_print_single('Output Root', args.o[0])
    pretty_print_single('Quality', args.cqp[0])
    pretty_print_pair('Rendering', args.render[0][0], args.render[0][1])
    if len(args.render) > 1:
        for job in args.render[1:]:
            pretty_print_pair('', job[0], job[1])
    pretty_print_single('Overwrite', args.overwrite)
    return

def main(args):
    for job in args.render:
        this_job = RenderJob(
            args.input_file,
            output_root=args.o[0],
            encoder_path=args.nvenc[0],
            cqp=args.cqp[0],
            output_res=job[1],
            codec=job[0]
        )
        this_job.render()
    return


# -- Run Main -- #
if __name__ == '__main__':
    args = parse_args()
    main(args)
