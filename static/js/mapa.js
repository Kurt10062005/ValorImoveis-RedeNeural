//===================================================
//AUTORES:
//  Felipe Kuznik Thome 
//  Kurt Cobain  Rodrigues 
//  Pedro Ghinzelli
//===================================================

//===================================================
// TESTES
//===================================================
console.log("NOVO MAPA.JS CARREGADO COM SUCESSO!");

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
// DADOS DAS CASAS ESPALHADAS (ID + POSIÇÃO Y, X)
// ==================================================
const casas = [
    { id: 1, posicao: [220, 600] },
    { id: 2, posicao: [280, 190] },
    { id: 3, posicao: [600, 210] },
    { id: 4, posicao: [444, 877] },
    { id: 5, posicao: [520, 520] }
];

// ==================================================
// ÍCONE DA CASA
// ==================================================
const iconeCasa = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconSize: [18, 30],
    iconAnchor: [9, 30]
});

// ==================================================
// PEGA A JANELA E BOTÃO
// ==================================================
const janelaCasa = document.getElementById("janelaCasa");
const fecharJanela = document.getElementById("fecharJanela");

// ==================================================
// CRIA OS MARCADORES NO MAPA
// ==================================================
casas.forEach(casa => {
    const marcador = L.marker(casa.posicao, { icon: iconeCasa }).addTo(mapa);

    // Ao clicar em um marcador específico, passa os dados dessa casa para a função
    marcador.on("click", function () {
        abrirJanelaCasa(casa);
    });
});

// ==================================================
// FUNÇÃO PARA ABRIR A JANELA
// ==================================================
function abrirJanelaCasa(casa) {
    const campoId = document.getElementById("casa_id");
    if (campoId) {
        campoId.value = casa.id; // Coloca o ID da casa clicada no campo da janela
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