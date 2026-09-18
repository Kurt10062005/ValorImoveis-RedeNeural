//===================================================
//AUTORES:
//  Felipe Kuznik Thome 
//  Kurt Cobain  Rodrigues 
//  Pedro Henrique Ghinzelli dos Nascimento
//===================================================

async function gerarSimulacaoAleatoria() {
    try {
        const resposta = await fetch('/simular-aleatorio');
        if (!resposta.ok) {
            throw new Error('Erro ao buscar dados aleatórios.');
        }

        const casa = await resposta.json();

        // Preenche o campo ID (caso existente)
        if (document.getElementById('simulacao_id')) {
            document.getElementById('simulacao_id').value = casa.id;
        }

        // Preenche os campos do formulário da direita (editáveis)
        document.getElementById('id').value = casa.id;
        document.getElementById('quartos').value = casa.quartos;
        document.getElementById('banheiros').value = casa.banheiros;
        document.getElementById('area_living').value = casa.area_living;
        document.getElementById('area_lote').value = casa.area_lote;
        document.getElementById('andares').value = casa.andares;
        document.getElementById('waterfront').value = casa.waterfront;
        document.getElementById('view').value = casa.view;
        document.getElementById('conservacao').value = casa.conservacao;
        document.getElementById('grade').value = casa.grade;
        document.getElementById('area_shove').value = casa.area_shove;
        document.getElementById('area_basement').value = casa.area_basement;
        document.getElementById('ano_construcao').value = casa.ano_construcao;
        document.getElementById('ano_reforma').value = casa.ano_reforma;
        document.getElementById('cep').value = casa.cep;
        document.getElementById('lat').value = casa.lat;
        document.getElementById('long').value = casa.long;
        document.getElementById('area_living15').value = casa.area_living15;
        document.getElementById('area_lote15').value = casa.area_lote15;
        document.getElementById('preco_real').value = casa.preco_real;

    } catch (erro) {
        console.error('Erro ao gerar simulação:', erro);
        alert('Não foi possível carregar os dados aleatórios.');
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const formData = new FormData(form);

            try {
                const resposta = await fetch("/enviar", {
                    method: "POST",
                    body: formData
                });

                if (!resposta.ok) {
                    throw new Error("Erro ao calcular o preço.");
                }

                const dados = await resposta.json();

                const valorFormatado = dados.preco_previsto.toLocaleString('pt-BR', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                });

                const elementoResultado = document.getElementById("resultado_preco");
                if (elementoResultado) {
                    elementoResultado.innerText = valorFormatado;
                }

            } catch (erro) {
                console.error("Erro na requisição:", erro);
                alert("Ocorreu um erro ao calcular o preço.");
            }
        });
    }
});