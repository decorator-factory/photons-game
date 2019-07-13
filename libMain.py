from main_blockSolid import main as BlockSolid
from main_blockMirror import main as BlockMirror
from main_blockScatterer import main as BlockScatterer
from main_blockLaser import main as BlockLaser
from main_blockLens import main as BlockLens
from main_blockSquareWave import main as BlockSquareWave
from main_blockButton import main as BlockButton

libData = {"name":"Main","desc":"Main library for Photons. Includes all the basic elements necessary for simulations.","author":"int6h","version":"1.0.0"}

__include__ = [BlockSolid, BlockMirror, BlockLens, BlockLaser, BlockScatterer, BlockSquareWave, BlockButton]
