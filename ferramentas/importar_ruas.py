"""Importa as ruas em destaque de um KML/KMZ exportado do Google My Maps.

Uso: python3 ferramentas/importar_ruas.py caminho/do/arquivo.kml|kmz [--raiz pasta-do-site]

Cada Placemark vira uma rua em `streets` no map-data do index.html: o id é o <name> sem
acentos, e a região (que define a cor) é a freguesia que contém a maior parte dos pontos do
traçado. O nome mostrado no site vem do `nome` em assets/conteudo/ruas.json; o <name> do KML
só serve para o id, então não o mude depois de escrever o texto. Placemarks com o mesmo nome
de um contorno de assets/maps/freguesias-porto.kml são ignorados, para o mesmo mapa do
My Maps poder guardar freguesias e ruas. O KML passa a ser a fonte das ruas: as que não estão
nele saem do mapa e do ruas.json. As ruas são guardadas em assets/maps/ruas-porto.kml.
"""
import argparse, json, re, sys, unicodedata, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {'k': 'http://www.opengis.net/kml/2.2'}


def slug(text):
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')


def coords(element):
    # KML: "lng,lat[,alt] lng,lat[,alt] ..."
    return [[round(float(x), 7) for x in point.split(',')[:2]] for point in element.text.split()]


def geometry(placemark):
    lines = [coords(c) for c in placemark.findall('.//k:LineString/k:coordinates', NS)]
    rings = [coords(c) for c in placemark.findall('.//k:Polygon/k:outerBoundaryIs//k:coordinates', NS)]
    if rings:
        return {'type': 'Polygon', 'coordinates': [rings[0]]}
    if len(lines) == 1:
        return {'type': 'LineString', 'coordinates': lines[0]}
    if lines:
        return {'type': 'MultiLineString', 'coordinates': lines}
    return None


def inside(lng, lat, ring):
    # ring em [lat,lng], como o `polygon` das regiões
    hit = False
    for (lat1, lng1), (lat2, lng2) in zip(ring, ring[1:] + ring[:1]):
        if (lat1 > lat) != (lat2 > lat) and lng < (lng2 - lng1) * (lat - lat1) / (lat2 - lat1) + lng1:
            hit = not hit
    return hit


def region_for(geom, regions):
    points = geom['coordinates']
    while isinstance(points[0][0], list):
        points = [p for part in points for p in part]
    counts = {r['id']: sum(inside(lng, lat, r['polygon']) for lng, lat in points) for r in regions}
    best = max(counts, key=counts.get)
    if counts[best]:
        return best
    lng = sum(p[0] for p in points) / len(points); lat = sum(p[1] for p in points) / len(points)
    return min(regions, key=lambda r: (r['center'][0] - lat) ** 2 + (r['center'][1] - lng) ** 2)['id']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('arquivo')
    parser.add_argument('--raiz', default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    root = Path(args.raiz)

    source = Path(args.arquivo)
    if source.suffix.lower() == '.kmz':
        with zipfile.ZipFile(source) as z:
            kml = z.read(next(n for n in z.namelist() if n.endswith('.kml')))
    else:
        kml = source.read_bytes()
    ET.register_namespace('', NS['k'])
    doc = ET.fromstring(kml)
    source_name = (doc.findtext('k:Document/k:name', '', NS) or source.stem).strip()
    outlines = ET.parse(root / 'assets/maps/freguesias-porto.kml').getroot()
    region_names = {(p.findtext('k:name', '', NS) or '').strip() for p in outlines.iter('{%s}Placemark' % NS['k'])}

    index_path = root / 'index.html'
    html = index_path.read_text(encoding='utf-8')
    m = re.search(r'(<script id="map-data" type="application/json">)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))

    streets, skipped = [], []
    for parent in list(doc.iter()):
        for placemark in parent.findall('k:Placemark', NS):
            if (placemark.findtext('k:name', '', NS) or '').strip() in region_names:
                parent.remove(placemark)
    for placemark in doc.iter('{%s}Placemark' % NS['k']):
        name = (placemark.findtext('k:name', '', NS) or '').strip()
        geom = geometry(placemark)
        if not name or not geom:
            skipped.append(name or '(sem nome)')
            continue
        id = slug(name)
        if any(s['id'] == id for s in streets):
            sys.exit('Duas ruas com o mesmo nome no KML: ' + name)
        streets.append({'id': id, 'name': name, 'regionId': region_for(geom, data['regions']),
                        'geometry': geom, 'sourceName': source_name})
    data['streets'] = streets
    html = html[:m.start(2)] + '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n' + html[m.end(2):]
    index_path.write_text(html, encoding='utf-8')

    ET.ElementTree(doc).write(root / 'assets/maps/ruas-porto.kml', encoding='UTF-8', xml_declaration=True)

    # ruas.json: um id que não existe em `streets` faria o arquivo inteiro ser rejeitado
    ruas_path = root / 'assets/conteudo/ruas.json'
    ruas = json.loads(ruas_path.read_text(encoding='utf-8'))
    ids = {s['id'] for s in streets}
    removed = [i['id'] for i in ruas['itens'] if i['id'] not in ids]
    ruas['itens'] = [i for i in ruas['itens'] if i['id'] in ids]
    ruas_path.write_text(json.dumps(ruas, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    with_text = {i['id'] for i in ruas['itens']}
    for s in streets:
        print(('   ' if s['id'] in with_text else 'sem texto ') + s['id'], '|', s['regionId'], '|', s['geometry']['type'])
    if skipped:
        print('Ignorados (sem nome ou sem linha/polígono):', ', '.join(skipped))
    if removed:
        print('Textos removidos do ruas.json:', ', '.join(removed))


if __name__ == '__main__':
    main()
