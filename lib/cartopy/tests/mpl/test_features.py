# Copyright Cartopy Contributors
#
# This file is part of Cartopy and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.

import matplotlib.pyplot as plt
import pytest

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.ogc_clients import _OWSLIB_AVAILABLE


@pytest.mark.filterwarnings("ignore:Downloading")
@pytest.mark.natural_earth
@pytest.mark.mpl_image_compare(filename='natural_earth.png')
def test_natural_earth():
    ax = plt.axes(projection=ccrs.PlateCarree())
    # NOTE: edgecolor is set to face for backwards compatibility with the
    #       the original image. If updating this test remove edgecolors for
    #       the filled features below (LAND, OCEAN, LAKES).
    ec = 'face'
    ax.add_feature(cfeature.LAND, edgecolor=ec)
    # To match with the old default style and not update an image
    ax.add_feature(cfeature.OCEAN, edgecolor=ec)
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5, edgecolor=ec)
    ax.add_feature(cfeature.RIVERS)
    ax.set_xlim((-20, 60))
    ax.set_ylim((-40, 40))
    return ax.figure


@pytest.mark.filterwarnings("ignore:Downloading")
@pytest.mark.natural_earth
@pytest.mark.mpl_image_compare(filename='natural_earth_custom.png')
def test_natural_earth_custom():
    ax = plt.axes(projection=ccrs.PlateCarree())
    feature = cfeature.NaturalEarthFeature('physical', 'coastline', '50m',
                                           edgecolor='black',
                                           facecolor='none')
    ax.add_feature(feature)
    ax.set_xlim((-26, -12))
    ax.set_ylim((58, 72))
    return ax.figure


@pytest.mark.mpl_image_compare(filename='gshhs_coastlines.png', tolerance=0.95)
def test_gshhs():
    ax = plt.axes(projection=ccrs.Mollweide())
    ax.set_extent([138, 142, 32, 42], ccrs.Geodetic())

    ax.stock_img()
    # Draw coastlines.
    ax.add_feature(cfeature.GSHHSFeature('coarse', edgecolor='red'))
    # Draw higher resolution lakes (and test overriding of kwargs)
    ax.add_feature(cfeature.GSHHSFeature('low', levels=[2],
                                         facecolor='green'), facecolor='blue')
    return ax.figure


@pytest.mark.network
@pytest.mark.skipif(not _OWSLIB_AVAILABLE, reason='OWSLib is unavailable.')
@pytest.mark.mpl_image_compare(filename='wfs.png')
def test_wfs():
    ax = plt.axes(projection=ccrs.OSGB(approx=True))
    url = 'https://nsidc.org/cgi-bin/atlas_south?service=WFS'
    typename = 'land_excluding_antarctica'
    feature = cfeature.WFSFeature(url, typename,
                                  edgecolor='red')
    ax.add_feature(feature)
    return ax.figure
