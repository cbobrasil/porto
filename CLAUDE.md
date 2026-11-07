# Guia do Porto (mapa interativo)

Site estático pessoal: um mapa por regiões de passeio, com listas de lugares, ruas em destaque e metrô. Feito para usar no celular, a pé. Publicado no GitHub Pages pelo workflow `.github/workflows/pages.yml`, que copia `index.html`, `.nojekyll` e `assets/` para o site; não há build.

Este projeto é uma cópia do **Guia de Madrid** (cbobrasil.github.io/madrid, pasta `../madrid`) adaptada para o Porto. Veja "Adaptar para outra cidade" para repetir o processo.

## Idioma e tom

- Interface e textos em **português do Brasil**. Nomes dos lugares ficam como no Porto (ex.: "Rua das Flores", "Torre dos Clérigos").
- Textos curtos e práticos, sem marketing. Nada de datas de viagem: o guia deve servir para qualquer pessoa.
- Texto de um local: o que é + um comentário sobre o tipo de comida, o que pedir ou o clima, e uma dica prática se houver (reservar, fila, dias fechados). Sem nota do Google. Exemplo: "Bufê vegano a preço fixo na Rua de Mouzinho da Silveira, entre São Bento e a Ribeira. Prato à vontade, sopa e sobremesa; prático para o almoço."
- Se não tiver certeza de que o lugar continua aberto, diga "confira antes de ir".
- Nada de endereços particulares (casas, apartamentos) no site: ele é público.

## Estrutura

- `index.html`: tudo. CSS no `<style>`, dados no bloco `<script id="map-data" type="application/json">`, lógica no último `<script>`. MapLibre GL JS 4.7.1 (unpkg) com tiles da OpenFreeMap (estilo positron).
- `assets/conteudo/bairros.json`, `locais.json`, `ruas.json`: textos editoriais, carregados em tempo de execução e sobrepostos aos dados do `index.html` pelo `id`. Formato: `{"versao":1,"tipo":"bairros|locais|ruas","itens":[{"id","nome","subtitulo"/"tipo"/"bairro","secoes":[{"titulo"?, "texto"?, "itens"?:[...]}],"links":[{"texto","url"}]}]}`. Um `id` que não existe no `index.html` faz o arquivo inteiro ser rejeitado. `ruas.json` está vazio por enquanto.
- `assets/maps/freguesias-porto.kml`: os 6 contornos desenhados no Google My Maps (todas as freguesias menos a do centro). No KML os nomes têm erros de digitação ("Lorderlo", "Bonfin"); os nomes corretos ficam no `map-data`.
- `assets/maps/metro.geojson`: linhas (`kind:"line"`, `line`, `color`, `name`, MultiLineString) e estações (`kind:"station"`, `name`, `lines:[...]`, Point), geradas do OpenStreetMap via Overpass.
- `fontes/`: arquivos de origem, que não vão para o site. `fontes/listas-google/*.csv` são as listas exportadas do Google Maps (sem coordenadas) e `fontes/freguesias-porto.kmz` é o export original do My Maps.

### Dados em `map-data`

- `groups`: centro, oeste, norte e leste, com a legenda de cada um.
- `regions[]`: as 7 freguesias do Porto. `id`, `name` (nome completo da freguesia), `mapLabel` (rótulo curto no mapa, ex.: "Foz"; tem prioridade sobre o `nome` do `bairros.json`), `group`, `color` (cores da bandeira arco-íris: #E40303, #FF8C00, #FFED00, #008026, #004DFF, #750787), `tag`, `center` [lat,lng], `polygon` [[lat,lng],...] (anel aberto), `geometry` GeoJSON opcional ([lng,lat], anel fechado; tem prioridade), além de `description`, `atmosphere`, `highlights`, `walk`, `tip`, `official`, `source` (Wikipédia), `sourceName`, `boundarySource`, `boundaryType`. O `centro-historico` vem da relação OSM 3382149 (`boundaryType: "official"`); as outras, do KML (`user-drawn`). O contador "N áreas" é calculado sozinho.
- `places[]`: `id`, `name`, `type` (categoria em português), `coords` [lat,lng], `symbol`, `base`, `listIds`, `googleUrl`, `sourceName` (título no CSV do Google).
  - Lugares das listas do Google usam `id` `google-<CID>`, onde o CID é o segundo número hexadecimal do link (`...:0x<CID>`) convertido para decimal.
  - `base: true` = referência fixa, mostrada pelo controle "Referências": São Bento (S), Torre dos Clérigos (C) e Ponte Luís I (P), com `anchor: true`.
  - `alwaysVisible: true` = sempre no mapa: o Terminal Intermodal de Campanhã (`busStation: true`, ícone de autocarro) e o aeroporto (`airport: true`, ícone de avião; fica fora do enquadramento de "Ver todas as áreas"). `hotel: true` também é suportado.
  - `isStreet` / `hideMarker` = sem ponto no mapa.
  - Todo o resto tem `base: false` e aparece só quando uma das suas listas está ativa.
- `placeLists[]`: `id`, `name`, `sourceName` (nome da lista no Google), `placeIds`. Listas atuais: bares e clubs LGBT+ (`lgbt`), vegano e vegetariano (`vegano`), estacionamentos (`estacionamentos`). Um lugar pode estar em várias.
- `streets[]`: `id`, `name`, `regionId` (define a cor), `geometry` (LineString/Polygon [lng,lat]), `sourceName`. Vazio por enquanto; a seção "Ruas em destaque" só aparece quando houver ruas.

### Comportamentos que vale saber

- Cor do ponto vem de `placeColor()` pelo texto do `type`: azul para museus e estabelecimentos, vermelho para praças e monumentos, verde para parques.
- O popup de um local tem os botões "Abrir no Google Maps" (`googleUrl` ou busca pelo nome + ", Porto") e "Como chegar" (`placeGoogleLinks()`).
- A seção Metrô na lateral fica sempre aberta, com uma caixa "Mostrar" que liga e desliga o metrô inteiro e botões por linha (A–F).
- O rodapé ("Como ler o mapa", "Sobre os contornos e as fontes", "Meus textos") fica em `<details>` fechados.
- Abrindo o `index.html` como arquivo (`file://`), os JSONs de texto e o metrô não carregam. Para testar: `python3 -m http.server 8001` e abrir http://localhost:8001 (a porta 8000 costuma estar ocupada pelo guia de Madrid).

## Como editar os dados

- Edite o bloco `map-data` com um script Python: extraia com regex, `json.loads`, altere e grave com `json.dumps(d, ensure_ascii=False, indent=2)`, que preserva o formato atual.
- Os JSONs de `assets/conteudo/` são gravados com `indent=2`, `ensure_ascii=False` e uma quebra de linha no final.
- Para adicionar lugares de um CSV do Google: o CSV não traz coordenadas. Elas saem da página do link (`/maps/place/...`), que tem um link `/maps/preview/place?...`; a resposta desse link contém `[null,null,<lat>,<lng>]` e o endereço. Use um User-Agent de navegador e o cookie de consentimento `SOCS`.
- Depois de mudar ids, confira se os `id` dos JSONs de conteúdo e as listas (`placeIds`, `listIds`) ainda batem com `places`, `regions` e `streets`.
- Ao adicionar ou remover regiões ou listas, atualize o README (número de regiões e nomes das listas).
- Commit e push só quando for pedido.

## Metrô

Gerado de `relation[type=route][route=light_rail][network="Metro do Porto"]` com `ref` de A a F (o Bx, expresso da B, fica de fora porque usa os mesmos trilhos). Muitas paragens não têm nó de estação no OSM, então as estações são os nós `stop` das rotas agrupados por nome (num raio de 350 m), na posição média. As cores vêm da tag `colour` das relações. Quando as linhas G e H aparecerem no OSM, gere o arquivo de novo.

## Adaptar para outra cidade

1. **Textos fixos no `index.html`**: `<title>`, `meta description`, `<h1>`, os `aria-label` da lateral e do mapa, `.map-caption`, o `<p>` do diálogo da região, os textos do rodapé (referências, chegada, símbolo do metrô) e o "N áreas" inicial.
2. **Código**: `center` na criação do mapa; `', Porto'` em `placeGoogleLinks()` e `', Porto, Portugal'` em `mapLink`; o `customAttribution` dos contornos; `metroStationIcon()`, que desenha o símbolo das estações.
3. **Dados**: substitua `groups`, `regions`, `places`, `placeLists`, `streets` e `boundaryAttribution` no `map-data`, e escolha as novas referências fixas e os pontos sempre visíveis. Recrie os três JSONs de `assets/conteudo/` com os novos ids e substitua os KMLs.
4. **Metrô**: gere um novo `metro.geojson` no mesmo formato, a partir do OpenStreetMap via Overpass (veja "Metrô"). O Overpass recusa pedidos sem User-Agent (HTTP 406). Para uma cidade sem metrô, remova a seção e o controle "Metrô".
5. **README.md** e nome do site ("Guia de <Cidade>").
6. **Publicação**: repositório próprio no GitHub, com Settings → Pages → Source: GitHub Actions. O workflow funciona sem mudanças.
