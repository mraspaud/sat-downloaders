"""Test dhus."""

from urllib.parse import urljoin

import responses

from sat_downloaders.dhus import DHUSDownloader


@responses.activate
def test_dhus():
    """Test dhus downloads."""
    server = "https://myhub.com/"
    query_args = ["producttype:GRD", "swathIdentifier:EW"]
    entry_patterns = dict(
        title_pattern=("{platform_name:3s}_{scan_mode:2s}_{type:4s}_{data_source:4s}_{start_time:%Y%m%dT%H%M%S}_"
                       "{end_time:%Y%m%dT%H%M%S}_{orbit_number:6d}_{random_string1:6s}_{random_string2:4s}"),
        filename_pattern=("{platform_name:3s}_{scan_mode:2s}_{type:4s}_{data_source:4s}_{start_time:%Y%m%dT%H%M%S}_"
                          "{end_time:%Y%m%dT%H%M%S}_{orbit_number:06d}_{random_string1:6s}_{random_string2:4s}.SAFE"))
    dhus = DHUSDownloader(server, query_args, entry_patterns)

    url = urljoin(server, 'search?q=producttype:GRD+AND+swathIdentifier:EW&rows=100&start=0')
    responses.get(
        url,
        body=sample_response_text
    )

    entries = dhus.query()
    assert len(entries) == 2


sample_response_text = """
<?xml version="1.0" ?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
	<title>Data Hub Service search results for: producttype:GRD AND swathIdentifier:EW</title>
	<subtitle>Displaying 2 results. Request done in 0.494 seconds.</subtitle>
	<updated>2022-08-26T09:24:51.647Z</updated>
	<author>
		<name>Data Hub Service</name>
	</author>
	<id>https://myhub.com/search?q=producttype:GRD AND swathIdentifier:EW</id>
	<opensearch:totalResults>2</opensearch:totalResults>
	<opensearch:startIndex>0</opensearch:startIndex>
	<opensearch:itemsPerPage>100</opensearch:itemsPerPage>
	<opensearch:Query startPage="1" searchTerms="producttype:GRD AND swathIdentifier:EW" role="request"/>
	<link href="https://myhub.com/search?q=producttype:GRD AND swathIdentifier:EW&amp;start=0&amp;rows=100" type="application/xml" rel="self"/>
	<link href="https://myhub.com/search?q=producttype:GRD AND swathIdentifier:EW&amp;start=0&amp;rows=100" type="application/xml" rel="first"/>
	<link href="https://myhub.com/search?q=producttype:GRD AND swathIdentifier:EW&amp;start=27&amp;rows=100" type="application/xml" rel="last"/>
	<link href="opensearch_description.xml" type="application/opensearchdescription+xml" rel="search"/>
	<entry>
		<title>S1A_IW_GRDH_1SDV_20220825T154204_20220825T154229_044711_05568E_665F</title>
		<link href="https://myhub.com/odata/v1/Products('b984a4c1-693c-4c35-944e-c2638873ad74')/$value"/>
		<link rel="alternative" href="https://myhub.com/odata/v1/Products('b984a4c1-693c-4c35-944e-c2638873ad74')/"/>
		<link rel="icon" href="https://myhub.com/odata/v1/Products('b984a4c1-693c-4c35-944e-c2638873ad74')/Products('Quicklook')/$value"/>
		<id>b984a4c1-693c-4c35-944e-c2638873ad74</id>
		<summary>Date: 2022-08-25T15:42:04.382Z, Instrument: SAR-C SAR, Mode: VV VH, Satellite: Sentinel-1, Size: 1.59 GB</summary>
		<ondemand>false</ondemand>
		<date name="beginposition">2022-08-25T15:42:04.382Z</date>
		<date name="endposition">2022-08-25T15:42:29.381Z</date>
		<date name="ingestiondate">2022-08-26T09:04:15.245Z</date>
		<int name="orbitnumber">44711</int>
		<int name="relativeorbitnumber">14</int>
		<int name="lastrelativeorbitnumber">14</int>
		<int name="lastorbitnumber">44711</int>
		<int name="missiondatatakeid">349838</int>
		<int name="slicenumber">5</int>
		<str name="sensoroperationalmode">IW</str>
		<str name="gmlfootprint">&lt;gml:Polygon srsName=&quot;http://www.opengis.net/gml/srs/epsg.xml#4326&quot; xmlns:gml=&quot;http://www.opengis.net/gml&quot;&gt;
   &lt;gml:outerBoundaryIs&gt;
      &lt;gml:LinearRing&gt;
         &lt;gml:coordinates&gt;65.672287,24.556368 66.137955,30.065588 64.651718,30.645807 64.199944,25.428974 65.672287,24.556368&lt;/gml:coordinates&gt;
      &lt;/gml:LinearRing&gt;
   &lt;/gml:outerBoundaryIs&gt;
&lt;/gml:Polygon&gt;</str>
		<str name="footprint">MULTIPOLYGON (((25.428974 64.199944, 30.645807 64.651718, 30.065588 66.137955, 24.556368 65.672287, 25.428974 64.199944)))</str>
		<str name="format">SAFE</str>
		<str name="platformname">Sentinel-1</str>
		<str name="filename">S1A_IW_GRDH_1SDV_20220825T154204_20220825T154229_044711_05568E_665F.SAFE</str>
		<str name="instrumentname">Synthetic Aperture Radar (C-band)</str>
		<str name="instrumentshortname">SAR-C SAR</str>
		<str name="size">1.59 GB</str>
		<str name="producttype">GRD</str>
		<str name="platformidentifier">2014-016A</str>
		<str name="orbitdirection">ASCENDING</str>
		<str name="identifier">S1A_IW_GRDH_1SDV_20220825T154204_20220825T154229_044711_05568E_665F</str>
		<str name="timeliness">NRT-3h</str>
		<str name="swathidentifier">IW</str>
		<str name="productclass">S</str>
		<str name="polarisationmode">VV VH</str>
		<str name="acquisitiontype">NOMINAL</str>
		<str name="status">ARCHIVED</str>
		<str name="uuid">b984a4c1-693c-4c35-944e-c2638873ad74</str>
	</entry>
	<entry>
		<title>S1A_IW_GRDH_1SDV_20220826T050814_20220826T050839_044719_0556E0_48B7</title>
		<link href="https://myhub.com/odata/v1/Products('786cafe0-18cd-4c65-a58e-219193c13aa5')/$value"/>
		<link rel="alternative" href="https://myhub.com/odata/v1/Products('786cafe0-18cd-4c65-a58e-219193c13aa5')/"/>
		<link rel="icon" href="https://myhub.com/odata/v1/Products('786cafe0-18cd-4c65-a58e-219193c13aa5')/Products('Quicklook')/$value"/>
		<id>786cafe0-18cd-4c65-a58e-219193c13aa5</id>
		<summary>Date: 2022-08-26T05:08:14.746Z, Instrument: SAR-C SAR, Mode: VV VH, Satellite: Sentinel-1, Size: 1.65 GB</summary>
		<ondemand>false</ondemand>
		<date name="beginposition">2022-08-26T05:08:14.746Z</date>
		<date name="endposition">2022-08-26T05:08:39.744Z</date>
		<date name="ingestiondate">2022-08-26T06:10:49.686Z</date>
		<int name="orbitnumber">44719</int>
		<int name="relativeorbitnumber">22</int>
		<int name="lastrelativeorbitnumber">22</int>
		<int name="lastorbitnumber">44719</int>
		<int name="missiondatatakeid">349920</int>
		<int name="slicenumber">13</int>
		<str name="sensoroperationalmode">IW</str>
		<str name="gmlfootprint">&lt;gml:Polygon srsName=&quot;http://www.opengis.net/gml/srs/epsg.xml#4326&quot; xmlns:gml=&quot;http://www.opengis.net/gml&quot;&gt;
   &lt;gml:outerBoundaryIs&gt;
      &lt;gml:LinearRing&gt;
         &lt;gml:coordinates&gt;55.029175,19.219368 55.450542,15.104211 56.943424,15.511952 56.517391,19.787035 55.029175,19.219368&lt;/gml:coordinates&gt;
      &lt;/gml:LinearRing&gt;
   &lt;/gml:outerBoundaryIs&gt;
&lt;/gml:Polygon&gt;</str>
		<str name="footprint">MULTIPOLYGON (((19.219368 55.029175, 19.787035 56.517391, 15.511952 56.943424, 15.104211 55.450542, 19.219368 55.029175)))</str>
		<str name="format">SAFE</str>
		<str name="platformname">Sentinel-1</str>
		<str name="filename">S1A_IW_GRDH_1SDV_20220826T050814_20220826T050839_044719_0556E0_48B7.SAFE</str>
		<str name="instrumentname">Synthetic Aperture Radar (C-band)</str>
		<str name="instrumentshortname">SAR-C SAR</str>
		<str name="size">1.65 GB</str>
		<str name="producttype">GRD</str>
		<str name="platformidentifier">2014-016A</str>
		<str name="orbitdirection">DESCENDING</str>
		<str name="identifier">S1A_IW_GRDH_1SDV_20220826T050814_20220826T050839_044719_0556E0_48B7</str>
		<str name="timeliness">NRT-3h</str>
		<str name="swathidentifier">IW</str>
		<str name="productclass">S</str>
		<str name="polarisationmode">VV VH</str>
		<str name="acquisitiontype">NOMINAL</str>
		<str name="status">ARCHIVED</str>
		<str name="uuid">786cafe0-18cd-4c65-a58e-219193c13aa5</str>
	</entry>
</feed>
"""  # noqa
