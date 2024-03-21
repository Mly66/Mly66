import sys
sys.path.append("../../")
import struct
import bz2
import gzip
import zipfile
import zstandard as zstd
import datetime
import os
import io
import numpy as np
from ..configure.location_config import radar_info

def _structure_size(structure):
    """计算structure的字节大小"""
    return struct.calcsize('<' + ''.join([i[1] for i in structure]))

def _unpack_from_buf(buf, pos, structure):
    '''unpack a structure from buf'''
    size = _structure_size(structure)
    return _unpack_structure(buf[pos:pos + size], structure), size

def _unpack_structure(string, structure):
    '''unpack a structure from a string'''
    '''unpack a structure from a string'''
    fmt = '<' + ''.join([i[1] for i in structure])
    lst = struct.unpack(fmt, string)
    return dict(zip([i[0] for i in structure], lst))

def _prepare_for_read(filename):
    """
    Return a file like object read for reading.
    Open a file for reading in binary mode with transparent decompression of
    Gzip and BZip2 files.  The resulting file-like object should be closed.
    Parameters
    ----------
    filename : str or file-like object
        Filename or file-like object which will be opened.  File-like objects
        will not be examined for compressed data.
    Returns
    -------
    file_like : file-like object
        File like object from which data can be read.
    """
    # if a file-like object was provided, return
    if hasattr(filename, 'read'):  # file-like object
        return filename
    # look for compressed data by examining the first few bytes
    if filename.lower().endswith('.zip'):
        fh = zipfile.ZipFile(filename, 'r')
        f = fh.open(fh.namelist()[0], mode='r')
        fh.close()
        magic = b'CDYW'
    elif filename.lower().endswith('.zst'):
        fh = open(filename, 'rb').read()
        dctx = zstd.ZstdDecompressor()
        ff = dctx.decompress(fh)
        f = io.BytesIO(ff)
        magic = b'CDYW'
    else:
        f = open(filename, 'rb')
        magic = f.read(3)
    if magic.startswith(b'\x1f\x8b'):
        f = gzip.GzipFile(filename, 'rb')
    elif magic.startswith(b'BZh'):
        f = bz2.BZ2File(filename, 'rb')
    elif magic == b'CDYW':
        return f
    else:
        f = open(filename, 'rb')
    return f

def julian2date(JulianDate, Msec, Hour=0):
    """
    faster than num2date in netcdf4
    :param JulianDate: Julian Date
    :param Msec: msec from 00:00
    :return:
    """
    deltday = datetime.timedelta(days=JulianDate)
    delHour = datetime.timedelta(hours=Hour)
    deltsec = datetime.timedelta(milliseconds=Msec)
    scantime = datetime.datetime(1969, 12, 31) + deltday + deltsec + delHour
    return scantime


def julian2date_SEC(Sec, Msec, Hour=0):
    """
    faster than num2date in netcdf4
    :param Sec: seconds
    :param Msec: microseconds
    :return:
    """
    deltSec = datetime.timedelta(seconds=Sec)
    deltHour = datetime.timedelta(hours=Hour)
    deltMSec = datetime.timedelta(microseconds=Msec)
    scantime = datetime.datetime(1970, 1, 1) + deltSec + deltMSec + deltHour
    return scantime

def get_radar_info(filename):
    """
    根据雷达名称找雷达的经纬度信息
    :param filename:
    :return:(lat(deg), lon(deg), elev(m), frequency(GHZ))
    """
    name = os.path.basename(filename)
    try:
        station_id = [int(name[idx:idx+4]) for idx in range(len(name)-4) if name[idx:idx+4].isdigit()][0]
    except Exception:
        station_id = 9911
    if station_id not in radar_info.index:
        station_id = 9911 ###找不到站点信息返回南京雷达
    return radar_info.loc[station_id, "Latitude"], radar_info.loc[station_id, "Longitude"],\
           radar_info.loc[station_id, "Elevation"], radar_info.loc[station_id, "Frequency"]

def get_radar_sitename(filename, station_id, id):
    name = os.path.basename(filename)
    if id:
        try:
            station_id = int(station_id[1:])
        except:
            return station_id
    else:
        station_id = [int(name[idx:idx + 4]) for idx in range(len(name) - 4) if name[idx:idx + 4].isdigit()][0]
    if station_id not in radar_info.index:
        station_id = 9911  ###找不到站点信息返回南京雷达
    return radar_info.loc[station_id, "Name"]

def _get_radar_type(filename, id, isfile=True):
    """
    根据雷达名称找雷达类型
    :param filename:
    :return:
    """
    if isfile:
        name = os.path.basename(filename)
        station_id = [int(name[idx:idx + 4]) for idx in range(len(name) - 4) if name[idx:idx + 4].isdigit()][0]
    else:
        station_id = id
    if station_id not in radar_info.index:
        return None
    Datatype = radar_info.loc[station_id, "Datatype"]
    if Datatype in ["SA", "SB", "CB", "SC", "CD"]:
        return "SAB"
    elif Datatype in ["CC", "CCJ"]:
        return "CC"
    else:
        return None

def radar_format(filename, id, isfile=True):
    if isfile:
        if hasattr(filename, 'read'):
            return filename
        fh = _prepare_for_read(filename)
        flag = fh.read(28)
        size = len(fh.read()) + 28
        fh.seek(100, 0)
        sc_flag = fh.read(9)
        fh.seek(116, 0)
        cc_flag = fh.read(9)
        fh.close()
        if flag[:4] == b'RSTM':
            return "WSR98D"
        elif flag[14:16] == b'\x01\x00':
            return "SAB"
        elif (size-1024)%3000 == 0 and (cc_flag == b"CINRAD/CC" or cc_flag == b"CINRAD-CC" or b"YLD3-D" in cc_flag):
            return "CC"
        elif (size-1024)%4000 == 0 and (sc_flag == b"CINRAD/SC" or sc_flag == b"CINRAD/CD"):
            return "SC"
        elif flag[8:12] == b'\x10\x00\x00\x00':
            return "PA"
        else:
            radar_type = _get_radar_type(filename, id=None, isfile=True)
            if radar_type is None:
                return 'YW-KA2'
            else:
                return radar_type
    else:
        radar_type = _get_radar_type(filename, id=id, isfile=False)
        if radar_type is None:
            return 'YW-KA2'
        else:
            return radar_type

def make_time_unit_str(dtobj):
    """ Return a time unit string from a datetime object. """
    return "seconds since " + dtobj.strftime("%Y-%m-%dT%H:%M:%SZ")


def cumsimp(y):
    """
    Simpson-rule column-wise cumulative summation.
    Transferred from MATLAT code by Kirill K. Pankratov, March 7, 1994.
    Parameters
    ----------
    y: (*array*) Input 2-D array.

    Returns: (*array*) Summation result.
    -------

    """
    # 3-points interpolation coefficients to midpoints.
    # Second-order polynomial (parabolic) interpolation coefficients
    # from  Xbasis = [0 1 2]  to  Xint = [.5 1.5]
    c1 = 3./8;  c2 = 6./8; c3 = -1./8

    # Determine the size of the input and make column if vector
    ist = 0         # If to be transposed
    lv = y.shape[0]
    if lv == 1:
        ist = 1
        y = y.T
        lv = len(y)
    f = np.zeros(y.shape)
    # If only 2 elements in columns - simple sum divided by 2
    if lv == 2:
        f[1, :] = (y[0, :] + y[1]) /2
        if ist:
            f = f.T
        return f

    # If more than two elements in columns - Simpson summation
    num = np.arange(0, lv-2)
    # Interpolate values of Y to all midpoints
    f[num+1, :] = c1 * y[num, :] + c2 * y[num+1, :] + c3 * y[num+2, :]
    f[num+2, :] = f[num+2, :] + c3 * y[num, :] + c2 * y[num+1, :] + c1 * y[num+2, :]
    f[1, :] = f[1, :] * 2
    f[lv - 1, :] = f[lv - 1, :] * 2

    # Now Simpson (1,4,1) rule
    f[1: lv, :] = 2 * f[1: lv, :] + y[0:lv-1, :] + y[1: lv, :]
    f = np.cumsum(f, axis=0) / 6  # Cumulative sum, 6 - denom. from the Simpson rule

    if ist:
        f = f.T
    return f


def flowfun(u, v):
    """
    Computes the potential PHI and the streamfunction PSI
     of a 2-dimensional flow defined by the matrices of velocity
     components U and V
    Parameters
    ----------
    param u: (*array*) U component of the wind. 2-D array.
    param v: (*array*) V component of the wind, 2-D array.

    Returns: (*array*) Stream function and potential velocity.
    -------
    """
    ly, lx = u.shape  # Size of the velocity matrices

    cx = cumsimp(u[0, :][np.newaxis, :])
    cy = cumsimp(v[:, 0][:, np.newaxis])
    phi = cumsimp(v) + np.tile(cx, [ly, 1])
    phi = (phi + cumsimp(u.T).T + np.tile(cy, [1, lx])) / 2

    # Compute streamfunction PSI (solenoidal part)
    cx = cumsimp(v[0, :][np.newaxis, :])
    cy = cumsimp(u[:, 0][:, np.newaxis])
    psi = -cumsimp(u) + np.tile(cx, [ly, 1])
    psi = (psi + cumsimp(v.T).T - np.tile(cy, [1, lx])) / 2
    return psi, phi


