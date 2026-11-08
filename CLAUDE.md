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
- `assets/conteudo/bairros.json`, `locais.json`, `ruas.json`: textos editoriais, carregados em tempo de execução e sobrepostos aos dados do `index.html` pelo `id`. Formato: `{"versao":1,"tipo":"bairros|locais|ruas","itens":[{"id","nome","subtitulo"/"tipo"/"bairro","secoes":[{"titulo"?, "texto"?, "itens"?:[...]}],"links":[{"texto","url"}]}]}`. Um `id` que não existe no `index.html` faz o arquivo inteiro ser rejeitado. No `ruas.json`, o `nome` é o nome mostrado no site (o `<name>` do KML só define o `id`).
- `assets/maps/freguesias-porto.kml`: os 6 contornos desenhados no Google My Maps (todas as freguesias menos a do centro). No KML os nomes têm erros de digitação ("Lorderlo", "Bonfin"); os nomes corretos ficam no `map-data`.
- `assets/maps/ruas-porto.kml`: os traçados das ruas em destaque, gravado por `ferramentas/importar_ruas.py` (não é lido pelo site; os traçados ficam em `streets`).
- `assets/maps/metro.geojson`: linhas (`kind:"line"`, `line`, `color`, `name`, MultiLineString) e estações (`kind:"station"`, `name`, `lines:[...]`, Point), geradas do OpenStreetMap via Overpass.
- `ferramentas/importar_ruas.py`: importa as ruas em destaque de um KML/KMZ do My Maps (veja "Ruas em destaque"). Não vai para o site.
- `fontes/`: arquivos de origem, que não vão para o site. `fontes/listas-google/*.csv` são as listas exportadas do Google Maps (sem coordenadas) e `fontes/freguesias-porto.kmz` é o export do mapa "Freguesias" do My Maps, com os 6 contornos e as ruas em destaque. `fontes/porto_tips.md` é um texto de dicas em inglês que originou as listas criadas à mão; os textos do site foram reescritos a partir dele.

### Dados em `map-data`

- `groups`: centro, oeste, norte e leste, com a legenda de cada um.
- `regions[]`: as 7 freguesias do Porto. `id`, `name` (nome completo da freguesia), `mapLabel` (rótulo curto no mapa, ex.: "Foz"; tem prioridade sobre o `nome` do `bairros.json`), `group`, `color` (tons de azul e cinza da marca "Porto.": #12306B, #2F5DB3, #3F8FC7, #1E7A9E, #8FA6C4, #4B5563, #6C7A8C), `tag`, `center` [lat,lng], `polygon` [[lat,lng],...] (anel aberto), `geometry` GeoJSON opcional ([lng,lat], anel fechado; tem prioridade), além de `description`, `atmosphere`, `highlights`, `walk`, `tip`, `official`, `source` (Wikipédia), `sourceName`, `boundarySource`, `boundaryType`. O `centro-historico` vem da relação OSM 3382149 (`boundaryType: "official"`); as outras, do KML (`user-drawn`). O contador "N áreas" é calculado sozinho.
- `places[]`: `id`, `name`, `type` (categoria em português), `coords` [lat,lng], `symbol`, `base`, `listIds`, `googleUrl`, `sourceName` (título no CSV do Google).
  - Lugares das listas do Google usam `id` `google-<CID>`, onde o CID é o segundo número hexadecimal do link (`...:0x<CID>`) convertido para decimal.
  - `base: true` = referência fixa, mostrada pelo controle "Referências": São Bento (S), Torre dos Clérigos (C), Ponte Luís I (P), Mercado do Bolhão (B), Livraria Lello (L), Casa da Música (CM), Jardins do Palácio de Cristal (PC) e Parque de Serralves (SV), todas com `anchor: true`. Serralves e Palácio de Cristal mantêm o `id` `google-…` e as listas.
  - `alwaysVisible: true` = sempre no mapa: o Terminal Intermodal de Campanhã (`busStation: true`, ícone de autocarro) e o aeroporto (`airport: true`, ícone de avião; fica fora do enquadramento de "Ver todas as áreas"). `hotel: true` também é suportado.
  - `isStreet` / `hideMarker` = sem ponto no mapa.
  - `lgbt: true` = lugar voltado ao público LGBT+: mostra uma bandeirinha arco-íris (CSS, `.lgbt-flag`) ao lado do nome no popup. Não existe lista LGBT+; esses lugares ficam em Bares ou Clubbing.
  - Todo o resto tem `base: false` e aparece só quando uma das suas listas está ativa.
- `placeLists[]`: `id`, `name`, `sourceName` (nome da lista no Google), `placeIds`. Listas atuais: monumentos (`monumentos`), museus (`museus`), igrejas e lugares religiosos (`igrejas`), parques e jardins (`parques`), pôr do sol (`por-do-sol`), restaurantes (`restaurantes`), bares (`bares`), clubbing (`clubbing`), casas de concertos (`concertos`), vegano e vegetariano (`vegano`), estacionamentos (`estacionamentos`). As listas de `monumentos` a `concertos` foram criadas à mão, não têm `sourceName` e foram preenchidas a partir de `fontes/porto_tips.md` (dicas em inglês, com links curtos `maps.app.goo.gl`; o redirecionamento do link já traz o CID e as coordenadas em `!3d`/`!4d`). Um lugar pode estar em várias, e uma referência fixa (`base: true`) também pode estar numa lista. O botão de uma lista sem lugares fica desativado.
- `streets[]`: `id`, `name`, `regionId` (define a cor), `geometry` (LineString/MultiLineString/Polygon [lng,lat]), `sourceName`. Gerado por `ferramentas/importar_ruas.py`; não edite à mão. Ruas atuais: Rua das Flores, Galeria de Paris (polígono) e Passeio das Virtudes. A seção "Ruas em destaque" só aparece quando houver ruas.

### Comportamentos que vale saber

- Cor do ponto vem de `placeColor()` pelo texto do `type`: azul para museus e estabelecimentos, cinza-ardósia para praças, monumentos e igrejas, verde-azulado para parques.
- O popup de um local tem os botões "Abrir no Google Maps" (`googleUrl` ou busca pelo nome + ", Porto") e "Como chegar" (`placeGoogleLinks()`).
- Hospedagem privada: um link com `#hospedagem=<lat>,<lng>` acrescenta um ponto "Hospedagem" (ícone H, `hotel: true`, sempre visível, entra no enquadramento de "Ver todas as áreas"). Só aceita coordenadas perto do Porto. Serve para mandar o mapa a amigos sem pôr o endereço no site: nunca grave essas coordenadas no repositório. O `#` não é enviado ao servidor.
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

## Ruas em destaque

Como no guia de Madrid. As ruas são desenhadas no mesmo mapa "Freguesias" do Google My Maps: uma linha por rua, ou um polígono para uma zona (como a Galeria de Paris). Exporte o mapa em KMZ e rode:

```
python3 ferramentas/importar_ruas.py ~/Downloads/Freguesias.kmz
```

O script:
- ignora os traçados com o mesmo nome de um contorno de `assets/maps/freguesias-porto.kml`;
- substitui `streets` no `map-data` pelo que está no arquivo (o KML é a fonte das ruas);
- gera o `id` a partir do nome do traçado, sem acentos (ex.: "Virtudes" → `virtudes`). Não renomeie um traçado depois de escrever o texto dele, ou o `id` muda;
- escolhe a região pela freguesia que contém a maior parte do traçado (ou a de centro mais próximo, se ficar fora de todas);
- grava os traçados em `assets/maps/ruas-porto.kml` e tira do `ruas.json` os textos de ruas que não existem mais;
- lista as ruas que ainda estão sem texto.

Depois, escreva os textos no `ruas.json` (`id`, `nome`, `bairro`, `secoes`, `links`, `origem`) no tom dos locais, guarde o KMZ em `fontes/freguesias-porto.kmz` e atualize o README.

## Metrô

Gerado de `relation[type=route][route=light_rail][network="Metro do Porto"]` com `ref` de A a F (o Bx, expresso da B, fica de fora porque usa os mesmos trilhos). Muitas paragens não têm nó de estação no OSM, então as estações são os nós `stop` das rotas agrupados por nome (num raio de 350 m), na posição média. As cores vêm da tag `colour` das relações. Quando as linhas G e H aparecerem no OSM, gere o arquivo de novo.

## Adaptar para outra cidade

1. **Textos fixos no `index.html`**: `<title>`, `meta description`, `<h1>`, os `aria-label` da lateral e do mapa, `.map-caption`, o `<p>` do diálogo da região, os textos do rodapé (referências, chegada, símbolo do metrô) e o "N áreas" inicial.
2. **Código**: `center` na criação do mapa; `', Porto'` em `placeGoogleLinks()` e `', Porto, Portugal'` em `mapLink`; o `customAttribution` dos contornos; `metroStationIcon()`, que desenha o símbolo das estações.
3. **Dados**: substitua `groups`, `regions`, `places`, `placeLists`, `streets` e `boundaryAttribution` no `map-data`, e escolha as novas referências fixas e os pontos sempre visíveis. Recrie os três JSONs de `assets/conteudo/` com os novos ids e substitua os KMLs.
4. **Metrô**: gere um novo `metro.geojson` no mesmo formato, a partir do OpenStreetMap via Overpass (veja "Metrô"). O Overpass recusa pedidos sem User-Agent (HTTP 406). Para uma cidade sem metrô, remova a seção e o controle "Metrô".
5. **README.md** e nome do site ("Guia de <Cidade>").
6. **Publicação**: repositório próprio no GitHub, com Settings → Pages → Source: GitHub Actions. O workflow funciona sem mudanças.
