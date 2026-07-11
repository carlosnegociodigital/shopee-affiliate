const input = document.querySelector("input[name='busca']");

const form = document.querySelector(".search-box");

const sugestoes = document.createElement("div");

sugestoes.className = "autocomplete";

form.appendChild(sugestoes);

input.addEventListener("input", async () => {

    const texto = input.value.trim();

    if(texto.length < 2){

        sugestoes.innerHTML = "";

        return;

    }

    const resposta = await fetch(`/buscar?busca=${encodeURIComponent(texto)}`);

    const dados = await resposta.json();

    sugestoes.innerHTML = "";

    dados.forEach(produto=>{

        const item = document.createElement("div");

        item.className = "item";

        item.innerText = produto.nome;

        item.onclick = ()=>{

            input.value = produto.nome;

            sugestoes.innerHTML = "";

            form.submit();

        }

        sugestoes.appendChild(item);

    });

});

document.addEventListener("click",(e)=>{

    if(!form.contains(e.target)){

        sugestoes.innerHTML="";

    }

});