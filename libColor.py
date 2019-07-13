from color_blockDecoupler import main as BlockDecoupler
from color_blockNegator import main as BlockNegator
from color_blockRemapper import main as BlockRemapper
from color_blockCoupler import main as BlockCoupler
from color_blockComparator import main as BlockComparator

libData = {"name":"Color","desc":"Color library for Photons. Provides some blocks that perform operations on beams' color.","author":"int6h","version":"1.0.0"}

__include__ = [BlockDecoupler, BlockNegator, BlockRemapper, BlockCoupler, BlockComparator]