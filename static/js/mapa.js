//===================================================
//AUTORES:
//  Felipe Kuznik Thome 
//  Kurt Cobain Rodrigues 
//  Pedro Henrique Ghinzelli do Nascimento
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
    minZoom: -0.5
});

// ==================================================
// LIMITES DO MAPA
// ==================================================
const limites = [[0, 0], [altura, largura]];

// ==================================================
// IMAGEM DO MAPA
// ==================================================
L.imageOverlay("/static/imagens/mapa.jpeg", limites).addTo(mapa);

// ==================================================
// AJUSTA O MAPA
// ==================================================
mapa.fitBounds(limites);
mapa.setMaxBounds(limites);

// ==================================================
// DADOS DOS MARCADORES
// ==================================================
// idMarcador = identificação interna do marcador

// dadosImovel = imóvel aleatório associado ao marcador
const marcadores = [
    { idMarcador: 1, posicao: [220, 600], dadosImovel: null },
    { idMarcador: 2, posicao: [280, 190], dadosImovel: null },
    { idMarcador: 3, posicao: [600, 210], dadosImovel: null },
    { idMarcador: 4, posicao: [444, 877], dadosImovel: null },
    { idMarcador: 5, posicao: [520, 520], dadosImovel: null },
    { idMarcador: 6, posicao: [100, 210], dadosImovel: null },
    { idMarcador: 7, posicao: [390, 522], dadosImovel: null },
    { idMarcador: 8, posicao: [470, 80], dadosImovel: null },
    { idMarcador: 9, posicao: [303, 50], dadosImovel: null },
    { idMarcador: 10, posicao: [570, 1033], dadosImovel: null },
    { idMarcador: 11, posicao: [400, 400], dadosImovel: null },
    { idMarcador: 12, posicao: [350, 770], dadosImovel: null },
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
// FUNÇÃO PARA PREENCHER AS INFORMAÇÕES DO IMÓVEL
// ==================================================
function preencherInformacoesImovel(marcador) {
    const dadosImovel = marcador.dadosImovel;

    // Verifica se existe um imóvel associado ao marcador
    if (!dadosImovel) {
        return;
    }

    // ==================================================
    // DADOS DO IMÓVEL
    // ==================================================
    document.getElementById("casa_id").value = dadosImovel.id;
    document.getElementById("casa_quartos").value = dadosImovel.quartos;
    document.getElementById("casa_banheiros").value = dadosImovel.banheiros;
    document.getElementById("casa_area_living").value = dadosImovel.area_living;
    document.getElementById("casa_area_lote").value = dadosImovel.area_lote;
    document.getElementById("casa_andares").value = dadosImovel.andares;
    document.getElementById("casa_waterfront").value = dadosImovel.waterfront == 1 ? "Sim" : "Não"; document.getElementById("casa_view").value = dadosImovel.view;
    const condicoes = {
        0: "C1 ➡️ Imóvel novo ou como novo",
        1: "C2 ➡️ Desgaste minimo de uso",
        2: "C3 ➡️ Desgaste normal do tempo",
        3: "C4 ➡️ Imóvel habitavel e funcionel",
        4: "C5 ➡️ Precisa de grandes reparos urgente",
        5: "C6 ➡️ Danos severos ou total falta de condições de moradia"
    };
    document.getElementById("casa_condicao").value = condicoes[dadosImovel.condicao];
    document.getElementById("casa_grade").value = dadosImovel.grade;
    document.getElementById("casa_area_shove").value = dadosImovel.area_shove;
    document.getElementById("casa_area_basement").value = dadosImovel.area_basement;
    document.getElementById("casa_ano_construcao").value = dadosImovel.ano_construcao;
    document.getElementById("casa_ano_reforma").value = dadosImovel.ano_reforma;
    document.getElementById("casa_cep").value = dadosImovel.cep;
    document.getElementById("casa_lat").value = dadosImovel.lat;
    document.getElementById("casa_long").value = dadosImovel.long;
    document.getElementById("casa_area_living15").value = dadosImovel.area_living15;
    document.getElementById("casa_area_lote15").value = dadosImovel.area_lote15;
    document.getElementById("casa_preco_real").value = dadosImovel.casa_preco_real;

    const valorFormatado = Number(dadosImovel.resultado_preco_mapa).toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });

    document.getElementById("resultado_preco_mapa").textContent = valorFormatado;
}

// ==================================================
// FUNÇÃO PARA BUSCAR UM IMÓVEL ALEATÓRIO
// ==================================================
async function buscarImovelAleatorio(marcador) {
    try {
        const resposta = await fetch("/simular-aleatorio-mapa");

        if (!resposta.ok) {
            throw new Error("Erro ao buscar imóvel aleatório.");
        }

        const dadosImovel = await resposta.json();

        // Guarda os dados do imóvel no marcador
        marcador.dadosImovel = dadosImovel;
        console.log("Marcador " + marcador.idMarcador + " recebeu o imóvel ID " + dadosImovel.id);
    } catch (erro) {
        console.error("Erro ao carregar imóvel do marcador " + marcador.idMarcador + ":", erro);
    }
}

// ==================================================
// CRIA OS MARCADORES NO MAPA
// ==================================================
marcadores.forEach(marcador => {
    const marcadorMapa = L.marker(marcador.posicao, { icon: iconeCasa }).addTo(mapa);

    // ==================================================
    // CLIQUE NO MARCADOR
    // ==================================================
    marcadorMapa.on("click", function () {
        abrirJanelaImovel(marcador);
    });
});

// ==================================================
// FUNÇÃO PARA ABRIR A JANELA DO IMÓVEL
// ==================================================
function abrirJanelaImovel(marcador) {
    // Verifica se os dados já foram carregados
    if (!marcador.dadosImovel) {
        alert("Os dados deste imóvel ainda estão sendo carregados.");
        return;
    }

    // Preenche a janela com os dados do imóvel
    preencherInformacoesImovel(marcador);

    // Abre a janela
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

// ==================================================
// CARREGA UM IMÓVEL ALEATÓRIO PARA CADA MARCADOR
// ==================================================
marcadores.forEach(marcador => {
    buscarImovelAleatorio(marcador);
});