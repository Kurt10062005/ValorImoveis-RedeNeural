//===================================================
//AUTORES:
//  Felipe Kuznik Thome 
//  Kurt Cobain  Rodrigues 
//  Pedro Ghinzelli
//===================================================

//===================================================
// TESTES
//===================================================
console.log("NOVO MAPA.JS CARREGADO COM SUCESSO!"); // Line para testar se atualizou

// ==================================================
// CONFIGURAÇÕES DO MAPA
// ==================================================
const largura = 1322;
const altura = 663;

// ==================================================
// CRIAÇÃO DO MAPA
// ==================================================
const mapa = L.map("mapa", {
    crs: L.CRS.Simple,
    minZoom: -1
});

// ==================================================
// LIMITES DO MAPA
// ==================================================
const limites = [
    [0, 0],
    [altura, largura]
];

// ==================================================
// IMAGEM DO MAPA
// ==================================================
L.imageOverlay(
    "/static/imagens/mapa.jpeg",
    limites
).addTo(mapa);

// ==================================================
// AJUSTA O MAPA
// ==================================================
mapa.fitBounds(limites);
mapa.setMaxBounds(limites);

// ==================================================
// DADOS DA CASA
// ==================================================
const casa = {
    id: 1,
    posicao: [220, 600]
};

// ==================================================
// ÍCONE DA CASA
// ==================================================
const iconeCasa = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

// ==================================================
// CRIA MARCADOR
// ==================================================
const marcador = L.marker(
    casa.posicao,
    {
        icon: iconeCasa
    }
).addTo(mapa);

// ==================================================
// PEGA A JANELA E BOTÃO
// ==================================================
const janelaCasa = document.getElementById("janelaCasa");
const fecharJanela = document.getElementById("fecharJanela");

// ==================================================
// CLIQUE NO MARCADOR (CORRIGIDO AQUI)
// ==================================================
marcador.on("click", function () {
    abrirJanelaCasa();
});

// ==================================================
// FUNÇÃO PARA ABRIR A JANELA
// ==================================================
function abrirJanelaCasa() {
    const campoId = document.getElementById("casa_id");
    if (campoId) {
        campoId.value = casa.id;
    }
    
    if (janelaCasa) {
        janelaCasa.style.display = "block";
    }
}

// ==================================================
// FECHAR A JANELA
// ==================================================
if (fecharJanela) {
    fecharJanela.addEventListener("click", function () {
        if (janelaCasa) {
            janelaCasa.style.display = "none";
        }
    });
}