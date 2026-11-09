# Guia do Porto

Um guia interativo para explorar o Porto a pé. O mapa reúne as freguesias da cidade, áreas desenhadas e listas de lugares para visitar, comer, sair à noite e estacionar.

Pensado principalmente para usar no celular durante os passeios.

## O que você encontra

- **7 regiões de passeio**, uma por freguesia do Porto, identificadas em tons de azul e cinza: Centro Histórico, Bonfim, Lordelo do Ouro e Massarelos, Aldoar/Foz do Douro/Nevogilde, Ramalde, Paranhos e Campanhã.
- **Fichas dos bairros** com descrição, clima e o que ver.
- **Pontos no mapa** com o nome do lugar e sua categoria.
- **Cores por categoria nos pontos:** verde-azulado para parques e jardins, cinza-ardósia para monumentos, praças e igrejas, azul para estabelecimentos e museus.
- **Ruas e áreas desenhadas no mapa**, com a cor da região, dentro das listas: ruas como Santa Catarina e Flores em "Ruas e praças", o Palácio da Bolsa em "Monumentos", os parques em "Parques e jardins", as estações em "Transportes". Toque numa delas para ler sobre ela.
- **Metro do Porto**: as linhas A a F com as cores oficiais e as estações marcadas com um "M" azul. Toque numa estação para ver as linhas que passam por ela.
- **Listas independentes** de pontos turísticos, monumentos, ruas e praças, museus, igrejas e lugares religiosos, parques e jardins, pôr do sol, restaurantes, tascas, bares, clubbing, concertos e eventos, LGBT+, vegano e vegetariano, transportes e estacionamentos. Os bares e clubs voltados ao público LGBT+ mostram uma bandeirinha arco-íris no popup, e a lista LGBT+ reúne todos eles. Os lugares veganos e vegetarianos aparecem no mapa como uma folhinha verde.
- **Sempre no mapa:** o ícone de transportes de Campanhã (comboios, metrô e autocarros), o aeroporto e os hospitais com urgência 24 horas (Santo António e São João, com uma cruz vermelha).

## Como explorar

Em **Minhas listas**, ative os assuntos que quer ver no mapa. É possível combinar várias listas; os lugares compartilhados aparecem uma única vez. Use **Ver listas ativas no mapa** para enquadrar a seleção.

Toque nos pontos para consultar as informações dos locais. Na lista de bairros, escolha uma região para ler sua ficha. No celular, a ficha ocupa a tela inteira; o **X** fecha e retorna ao mapa, mantendo as listas ativadas.

No celular, arraste a alça acima de **Guia do Porto** para cima para expandir a lista de bairros e para baixo para voltar ao mapa. Também é possível tocar na alça para alternar os tamanhos.

Os controles **Áreas**, **Nomes** e **Metrô** permitem ajustar o que aparece no mapa. Na seção **Metrô** da lista, que fica sempre aberta, escolha quais linhas aparecem (ou use **Todas** / **Nenhuma**); a caixa **Mostrar** liga e desliga o metrô inteiro.

## Sobre o mapa

Seis contornos foram desenhados no Google My Maps sobre as freguesias do Porto; o do Centro Histórico é o limite oficial da freguesia, tirado do OpenStreetMap. Os nomes dos lugares ficam como no Porto, e os textos do guia estão em português do Brasil.

É necessário acesso à internet para carregar o mapa de fundo.

Mapa exibido com [MapLibre GL JS](https://maplibre.org/) e [OpenFreeMap](https://openfreemap.org/), com dados do [OpenStreetMap](https://www.openstreetmap.org/copyright) e [OpenMapTiles](https://openmaptiles.org/). As seleções de lugares vieram de listas pessoais do Google Maps.

## Testar localmente

```
python3 -m http.server 8001
```

Depois abra http://localhost:8001. Abrindo o `index.html` direto como arquivo, os textos e o metrô não carregam.
