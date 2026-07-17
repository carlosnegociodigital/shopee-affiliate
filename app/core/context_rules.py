"""
Regras de contexto.

Cada categoria contém expressões compostas que possuem alta precisão.

Estas regras são verificadas ANTES das regras normais e da pontuação.

Quanto mais específica a expressão, menor a chance de erro.
"""

CONTEXT_RULES = {

    # =====================================================
    # CELULARES
    # =====================================================

    "Celulares": [

        "iphone",
        "iphone pro",
        "iphone plus",
        "iphone max",
        "iphone se",

        "galaxy s",
        "galaxy a",
        "galaxy note",

        "redmi note",
        "redmi",
        "poco x",
        "poco f",

        "moto g",
        "moto edge",

        "smartphone",

        "capinha iphone",
        "capinha samsung",
        "película iphone",
        "película samsung",
        "carregador iphone",
        "carregador samsung",
        "power bank",
        "cabo usb c",
        "cabo lightning",

    ],

    # =====================================================
    # INFORMÁTICA
    # =====================================================

    "Informática": [

        "notebook gamer",
        "notebook dell",
        "notebook lenovo",

        "placa mãe",
        "placa mae",

        "placa de vídeo",
        "placa de video",

        "memória ram",
        "memoria ram",

        "ssd nvme",
        "ssd sata",

        "hd externo",

        "processador intel",
        "processador amd",

        "intel core",
        "amd ryzen",

        "monitor gamer",
        "monitor ultrawide",

        "webcam",

        "mouse sem fio",
        "teclado mecânico",
        "teclado mecanico",

    ],

    # =====================================================
    # GAMER
    # =====================================================

    "Gamer": [

        "cadeira gamer",
        "mesa gamer",

        "mouse gamer",
        "teclado gamer",

        "headset gamer",

        "controle xbox",
        "controle ps5",
        "controle ps4",

        "playstation",
        "xbox series",
        "xbox one",

        "nintendo switch",

        "rgb gamer",

    ],

    # =====================================================
    # ELETRÔNICOS
    # =====================================================

    "Eletrônicos": [

        "smart tv",
        "android tv",

        "tv oled",
        "tv qled",
        "tv led",

        "caixa de som",
        "soundbar",

        "home theater",

        "projetor",

        "caixa bluetooth",

    ],

    # =====================================================
    # COZINHA
    # =====================================================

    "Cozinha": [

        "air fryer",
        "fritadeira elétrica",
        "fritadeira eletrica",

        "cafeteira",

        "liquidificador",

        "batedeira",

        "espremedor",

        "panela elétrica",
        "panela eletrica",

        "panela pressão",
        "panela de pressão",

        "microondas",
        "micro-ondas",

        "forno elétrico",

        "cooktop",

        "coifa",

        "sanduicheira",

        "grill elétrico",

    ],

    # =====================================================
    # CASA
    # =====================================================

    "Casa": [

        "ventilador",

        "ar condicionado",

        "aspirador robô",
        "aspirador robo",

        "aspirador de pó",

        "rodo",

        "vassoura",

        "organizador",

        "cabide",

        "cortina",

        "tapete",

        "luminária",

        "abajur",

    ],

    # =====================================================
    # BELEZA
    # =====================================================

    "Beleza": [

        "máscara facial",
        "máscara capilar",
        "máscara de cílios",

        "creme facial",
        "creme corporal",

        "hidratante facial",

        "protetor solar",

        "perfume feminino",
        "perfume masculino",

        "base líquida",

        "batom",

        "shampoo",

        "condicionador",

        "escova secadora",

        "chapinha",

        "secador de cabelo",

    ],

    # =====================================================
    # MODA
    # =====================================================

    "Moda": [

        "camiseta masculina",
        "camiseta feminina",

        "calça jeans",

        "vestido feminino",

        "bermuda masculina",

        "tênis masculino",
        "tênis feminino",

        "sandália feminina",

        "chinelo havaianas",

        "jaqueta",

    ],

    # =====================================================
    # PETS
    # =====================================================

    "Pets": [

        "ração cachorro",
        "ração gato",

        "coleira cachorro",

        "comedouro pet",

        "bebedouro pet",

        "areia gato",

        "brinquedo cachorro",

    ],

    # =====================================================
    # INFANTIL
    # =====================================================

    "Infantil": [

        "paper toy",

        "fantasia infantil",

        "fantasia halloween",

        "frankenstein",

        "dracula",

        "lobisomem",

        "vampiro",

        "brinquedo educativo",

        "quebra cabeça",

        "quebra-cabeça",

        "boneca",

        "carrinho brinquedo",

        "lego",

        "slime",

        "massinha",

        "mamadeira",

        "fralda",

        "carrinho bebê",

    ],

    # =====================================================
    # ESPORTES
    # =====================================================

    "Esportes": [

        "halter",

        "peso academia",

        "bicicleta",

        "esteira",

        "bola futebol",

        "bola basquete",

        "luva academia",

        "faixa elástica",

        "corda pular",

    ],

}