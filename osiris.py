#!/usr/bin/python3

from pathlib import Path
import torrent_parser as tp
from torf import Torrent
from torf import PieceSizeError
from torf import PathError
import humanfriendly as hf
import hashlib
import os
import sys

find_pieces = []
piece_sizes = ['32KiB','64KiB','128KiB','256KiB','512KiB','1MiB','2MiB','4MiB','8MiB','16MiB']

""" Buffer torrent to complete; put pieces in list """
target_torrent_path = '/home/opsoyo/AddedTorBackup/BA1CE55001D6268D3926F32DB03CC14243137080.torrent'
target_data_path = '/home/opsoyo/files/downloads/incomplete/PUBLIC DATABASES.rar'
target_torrent = Torrent.read(target_torrent_path)
target_pieces = target_torrent.hashes
for piece in target_pieces:
    piece_str = hashlib.sha1(piece).hexdigest()
    find_pieces.append(piece_str)
print('INFO: Buffered {} pieces for {}'.format(len(find_pieces),target_torrent_path))


"""
Scan random files from specified directory for pieces
that will work within target torrent above.
"""
arbpaths = Path('/home/opsoyo/files').glob('**/*')
for arbpath in arbpaths:
    arbpath_str = str(arbpath)
    if arbpath_str == target_data_path:
        print('INFO: Skipping target file(s) in scan.')
        continue
    if Path(arbpath_str).is_file():
        filename = os.path.basename(arbpath_str)

        # Binary hashes of whole file
        #
        #

        # Generate torrent with piece hashes
        for ps in piece_sizes:
            ps_bytes = hf.parse_size(ps)
            try:
                newt = Torrent(path=arbpath_str, piece_size=ps_bytes)
                newt.generate()
                newt_pieces = newt.hashes
                #firstpiece = hashlib.sha1(newt.hashes[0]).hexdigest()
            except PieceSizeError:
                print('ERROR: Piece size out of bounds.')
                continue
            except PathError:
                print('ERROR: File was empty or all were excluded.')
                continue
            except RuntimeError:
                print('ERROR: Something about too many pieces hashes.')
                continue

            for piece in newt_pieces:
                if piece in target_pieces:
                    print('INFO: Piece match identified: {} at {} for {}'.format(piece,ps_bytes,arbpath_str))


        #exit()
