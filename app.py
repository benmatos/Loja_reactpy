from reactpy import component, html, hooks, run
from reactpy_router import route, simple
from dataclasses import dataclass
from typing import List, Dict
import random

# ========== MODELS ==========

@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    image_url: str
    category: str
    stock: int
    rating: float = 0.0

@dataclass
class CartItem:
    product: Product
    quantity: int

class ShoppingCart:
    def __init__(self):
        self.items: Dict[int, CartItem] = {}
    
    def add_item(self, product: Product, quantity: int = 1):
        if product.id in self.items:
            self.items[product.id].quantity += quantity
        else:
            self.items[product.id] = CartItem(product, quantity)
    
    def remove_item(self, product_id: int):
        if product_id in self.items:
            del self.items[product_id]
    
    def update_quantity(self, product_id: int, quantity: int):
        if product_id in self.items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                self.items[product_id].quantity = quantity
    
    def get_total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items.values())
    
    def get_items_count(self) -> int:
        return sum(item.quantity for item in self.items.values())
    
    def clear(self):
        self.items.clear()

@dataclass
class User:
    id: int
    name: str
    email: str
    address: str
    phone: str

class UserSession:
    def __init__(self):
        self.current_user: User = None
        self.is_logged_in: bool = False
    
    def login(self, user: User):
        self.current_user = user
        self.is_logged_in = True
    
    def logout(self):
        self.current_user = None
        self.is_logged_in = False

# ========== CONTROLLERS ==========

class ProductController:
    def __init__(self):
        self.products: List[Product] = []
        self.filtered_products: List[Product] = []
        self.current_category: str = "all"
    
    def load_products(self, products: List[Product]):
        self.products = products
        self.filtered_products = products
    
    def filter_by_category(self, category: str):
        self.current_category = category
        if category == "all":
            self.filtered_products = self.products
        else:
            self.filtered_products = [
                p for p in self.products if p.category.lower() == category.lower()
            ]
    
    def search_products(self, query: str):
        query = query.lower()
        self.filtered_products = [
            p for p in self.products 
            if query in p.name.lower() or query in p.description.lower()
        ]
    
    def get_product_by_id(self, product_id: int) -> Product:
        for product in self.products:
            if product.id == product_id:
                return product
        return None

class CartController:
    def __init__(self):
        self.cart = ShoppingCart()
    
    def add_to_cart(self, product: Product, quantity: int = 1):
        self.cart.add_item(product, quantity)
    
    def remove_from_cart(self, product_id: int):
        self.cart.remove_item(product_id)
    
    def update_cart_quantity(self, product_id: int, quantity: int):
        self.cart.update_quantity(product_id, quantity)
    
    def get_cart_total(self) -> float:
        return self.cart.get_total()
    
    def get_cart_items_count(self) -> int:
        return self.cart.get_items_count()
    
    def clear_cart(self):
        self.cart.clear()

# ========== SAMPLE DATA ==========

def get_sample_products():
    return [
        Product(
            id=1,
            name="Smartphone XYZ",
            description="Smartphone com tela de 6.5 polegadas, 128GB, câmera tripla",
            price=899.99,
            image_url="https://images.unsplash.com/photo-1598327105854-c8674faddf74?w=300",
            category="eletronicos",
            stock=15,
            rating=4.5
        ),
        Product(
            id=2,
            name="Notebook ABC",
            description="Notebook i5, 8GB RAM, SSD 256GB, tela 15.6 polegadas",
            price=2499.99,
            image_url="https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=300",
            category="eletronicos",
            stock=8,
            rating=4.8
        ),
        Product(
            id=3,
            name="Camiseta Básica",
            description="Camiseta 100% algodão, diversas cores, confortável e durável",
            price=29.99,
            image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300",
            category="roupas",
            stock=50,
            rating=4.3
        ),
        Product(
            id=4,
            name="Tênis Esportivo",
            description="Tênis para corrida, amortecimento premium, design moderno",
            price=199.99,
            image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300",
            category="calcados",
            stock=20,
            rating=4.6
        ),
        Product(
            id=5,
            name="Livro Python Avançado",
            description="Livro sobre programação Python avançada, 400 páginas",
            price=59.99,
            image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=300",
            category="livros",
            stock=30,
            rating=4.7
        ),
        Product(
            id=6,
            name="Fone Bluetooth",
            description="Fone sem fio com cancelamento de ruído, bateria de 20h",
            price=159.99,
            image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300",
            category="eletronicos",
            stock=25,
            rating=4.4
        ),
        Product(
            id=7,
            name="Mochila Executiva",
            description="Mochila resistente à água, compartimento para notebook",
            price=129.99,
            image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300",
            category="acessorios",
            stock=18,
            rating=4.2
        ),
        Product(
            id=8,
            name="Smartwatch",
            description="Relógio inteligente com monitor de frequência cardíaca",
            price=299.99,
            image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300",
            category="eletronicos",
            stock=12,
            rating=4.9
        )
    ]

def get_sample_user():
    return User(
        id=1,
        name="João Silva",
        email="joao@email.com",
        address="Rua das Flores, 123 - São Paulo, SP",
        phone="(11) 99999-9999"
    )

# ========== VIEW COMPONENTS ==========

@component
def Header(cart_controller, user_session, set_show_cart, set_current_page):
    cart_items_count = cart_controller.get_cart_items_count()
    
    return html.header(
        {
            "class": "bg-blue-600 text-white p-4 shadow-md sticky top-0 z-10"
        },
        html.div(
            {
                "class": "container mx-auto flex justify-between items-center"
            },
            html.div(
                {
                    "class": "flex items-center space-x-4"
                },
                html.h1(
                    {
                        "class": "text-2xl font-bold cursor-pointer",
                        "on_click": lambda event: set_current_page("home")
                    },
                    "🛒 E-Store"
                ),
                html.nav(
                    {
                        "class": "hidden md:flex space-x-4"
                    },
                    html.a(
                        {
                            "class": "hover:text-blue-200 cursor-pointer",
                            "on_click": lambda event: set_current_page("home")
                        },
                        "Home"
                    ),
                    html.a(
                        {
                            "class": "hover:text-blue-200 cursor-pointer",
                            "on_click": lambda event: set_current_page("products")
                        },
                        "Produtos"
                    )
                )
            ),
            html.div(
                {
                    "class": "flex items-center space-x-4"
                },
                html.div(
                    {
                        "class": "relative cursor-pointer",
                        "on_click": lambda event: set_show_cart(True)
                    },
                    html.span("🛒"),
                    html.span(
                        {
                            "class": "absolute -top-2 -right-2 bg-red-500 rounded-full w-5 h-5 flex items-center justify-center text-xs"
                        },
                        f"{cart_items_count}"
                    ) if cart_items_count > 0 else ""
                ),
                html.div(
                    {
                        "class": "flex items-center space-x-2"
                    },
                    html.span(
                        {"class": "hidden md:inline"},
                        f"Olá, {user_session.current_user.name.split()[0]}" if user_session.is_logged_in else "Visitante"
                    ),
                    html.span(
                        {
                            "class": "bg-blue-500 rounded-full w-8 h-8 flex items-center justify-center"
                        },
                        "👤"
                    )
                )
            )
        )
    )

@component
def ProductCard(product, on_add_to_cart):
    return html.div(
        {
            "class": "bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow flex flex-col h-full"
        },
        html.img(
            {
                "src": product.image_url,
                "alt": product.name,
                "class": "w-full h-48 object-cover"
            }
        ),
        html.div(
            {
                "class": "p-4 flex flex-col flex-grow"
            },
            html.h3(
                {
                    "class": "text-lg font-semibold mb-2"
                },
                product.name
            ),
            html.p(
                {
                    "class": "text-gray-600 mb-2 text-sm flex-grow"
                },
                product.description[:80] + "..." if len(product.description) > 80 else product.description
            ),
            html.div(
                {
                    "class": "flex justify-between items-center mb-3"
                },
                html.span(
                    {
                        "class": "text-2xl font-bold text-blue-600"
                    },
                    f"R$ {product.price:.2f}"
                ),
                html.span(
                    {
                        "class": "text-sm text-gray-500"
                    },
                    f"Estoque: {product.stock}"
                )
            ),
            html.div(
                {
                    "class": "flex items-center mb-3"
                },
                html.span(
                    {
                        "class": "text-yellow-500 mr-1"
                    },
                    "★" * int(product.rating)
                ),
                html.span(
                    {
                        "class": "text-gray-400"
                    },
                    "★" * (5 - int(product.rating))
                ),
                html.span(
                    {
                        "class": "text-sm text-gray-600 ml-2"
                    },
                    f"({product.rating})"
                )
            ),
            html.button(
                {
                    "class": "w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors",
                    "on_click": lambda: on_add_to_cart(product)
                },
                "Adicionar ao Carrinho"
            )
        )
    )

@component
def CartSidebar(show_cart, set_show_cart, cart_controller):
    cart_items = cart_controller.cart.items.values()
    
    def handle_remove_item(product_id):
        cart_controller.remove_from_cart(product_id)
    
    def handle_quantity_change(product_id, new_quantity):
        cart_controller.update_cart_quantity(product_id, new_quantity)
    
    return html.div(
        {
            "class": f"fixed top-0 right-0 h-full w-80 bg-white shadow-lg transform transition-transform z-20 {'translate-x-0' if show_cart else 'translate-x-full'}"
        },
        html.div(
            {
                "class": "p-4 border-b flex justify-between items-center"
            },
            html.h2(
                {
                    "class": "text-xl font-semibold"
                },
                "🛒 Seu Carrinho"
            ),
            html.button(
                {
                    "class": "text-gray-500 hover:text-gray-700",
                    "on_click": lambda event: set_show_cart(False)
                },
                "✕"
            )
        ),
        html.div(
            {
                "class": "p-4 overflow-y-auto h-3/4"
            },
            [html.div(
                {
                    "key": item.product.id,
                    "class": "border-b py-4"
                },
                html.div(
                    {
                        "class": "flex"
                    },
                    html.img(
                        {
                            "src": item.product.image_url,
                            "alt": item.product.name,
                            "class": "w-16 h-16 object-cover rounded"
                        }
                    ),
                    html.div(
                        {
                            "class": "ml-4 flex-grow"
                        },
                        html.h3(
                            {
                                "class": "font-semibold"
                            },
                            item.product.name
                        ),
                        html.p(
                            {
                                "class": "text-blue-600 font-semibold"
                            },
                            f"R$ {item.product.price:.2f}"
                        ),
                        html.div(
                            {
                                "class": "flex items-center mt-2"
                            },
                            html.button(
                                {
                                    "class": "bg-gray-200 w-6 h-6 rounded flex items-center justify-center",
                                    "on_click": lambda event, id=item.product.id: handle_quantity_change(id, item.quantity - 1)
                                },
                                "−"
                            ),
                            html.span(
                                {
                                    "class": "mx-2"
                                },
                                f"{item.quantity}"
                            ),
                            html.button(
                                {
                                    "class": "bg-gray-200 w-6 h-6 rounded flex items-center justify-center",
                                    "on_click": lambda event, id=item.product.id: handle_quantity_change(id, item.quantity + 1)
                                },
                                "+"
                            ),
                            html.button(
                                {
                                    "class": "ml-4 text-red-500 hover:text-red-700",
                                    "on_click": lambda event, id=item.product.id: handle_remove_item(id)
                                },
                                "Remover"
                            )
                        )
                    )
                )
            ) for item in cart_items]
        ) if cart_items else html.div(
            {
                "class": "text-center py-8 text-gray-500"
            },
            "Seu carrinho está vazio"
        ),
        html.div(
            {
                "class": "absolute bottom-0 left-0 right-0 p-4 border-t bg-white"
            },
            html.div(
                {
                    "class": "flex justify-between text-lg font-semibold mb-4"
                },
                html.span("Total:"),
                html.span(f"R$ {cart_controller.get_cart_total():.2f}")
            ),
            html.button(
                {
                    "class": "w-full bg-green-600 text-white py-3 rounded font-semibold hover:bg-green-700"
                },
                "Finalizar Compra"
            )
        )
    )

@component
def HomePage(product_controller, cart_controller):
    categories = ["all", "eletronicos", "roupas", "calcados", "livros", "acessorios"]
    search_query, set_search_query = hooks.use_state("")
    
    def handle_search(event):
        set_search_query(event["target"]["value"])
        if event["target"]["value"]:
            product_controller.search_products(event["target"]["value"])
        else:
            product_controller.filter_by_category("all")
    
    def handle_category_change(category):
        product_controller.filter_by_category(category)
        set_search_query("")
    
    def handle_add_to_cart(product):
        cart_controller.add_to_cart(product)
    
    featured_products = random.sample(product_controller.products, min(3, len(product_controller.products)))
    
    return html.div(
        {
            "class": "container mx-auto p-4"
        },
        # Banner
        html.div(
            {
                "class": "bg-blue-100 rounded-lg p-8 mb-8 text-center"
            },
            html.h2(
                {
                    "class": "text-3xl font-bold text-blue-800 mb-4"
                },
                "Bem-vindo à E-Store!"
            ),
            html.p(
                {
                    "class": "text-blue-600 mb-6"
                },
                "Encontre os melhores produtos com os melhores preços"
            ),
            html.button(
                {
                    "class": "bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
                },
                "Ver Ofertas"
            )
        ),
        
        # Destaques
        html.h2(
            {
                "class": "text-2xl font-bold mb-6"
            },
            "Produtos em Destaque"
        ),
        html.div(
            {
                "class": "grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
            },
            [ProductCard(product, handle_add_to_cart) for product in featured_products]
        ),
        
        # Todos os produtos
        html.div(
            {
                "class": "mb-6"
            },
            html.h2(
                {
                    "class": "text-2xl font-bold mb-4"
                },
                "Nossos Produtos"
            ),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Buscar produtos...",
                    "value": search_query,
                    "on_change": handle_search,
                    "class": "w-full p-3 border border-gray-300 rounded-lg mb-4"
                }
            ),
            html.div(
                {
                    "class": "flex space-x-2 overflow-x-auto pb-2"
                },
                *[
                    html.button(
                        {
                            "key": cat,
                            "class": f"px-4 py-2 rounded-full whitespace-nowrap {'bg-blue-600 text-white' if product_controller.current_category == cat else 'bg-gray-200 text-gray-700'}",
                            "on_click": lambda event, cat=cat: handle_category_change(cat)
                        },
                        "Todos" if cat == "all" else cat.capitalize()
                    )
                    for cat in categories
                ]
            )
        ),
        html.div(
            {
                "class": "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            },
            *[
                ProductCard(product, handle_add_to_cart)
                for product in product_controller.filtered_products
            ]
        ) if product_controller.filtered_products else html.p(
            {
                "class": "text-center text-gray-500 text-lg"
            },
            "Nenhum produto encontrado."
        )
    )

@component
def ProductDetailPage(product_id, product_controller, cart_controller):
    product = product_controller.get_product_by_id(product_id)
    
    if not product:
        return html.div(
            {
                "class": "container mx-auto p-4 text-center"
            },
            html.h1("Produto não encontrado"),
            html.p("O produto que você está procurando não existe.")
        )
    
    def handle_add_to_cart():
        cart_controller.add_to_cart(product)
    
    return html.div(
        {
            "class": "container mx-auto p-4"
        },
        html.div(
            {
                "class": "grid grid-cols-1 md:grid-cols-2 gap-8"
            },
            html.div(
                html.img(
                    {
                        "src": product.image_url,
                        "alt": product.name,
                        "class": "w-full rounded-lg shadow-md"
                    }
                )
            ),
            html.div(
                html.h1(
                    {
                        "class": "text-3xl font-bold mb-4"
                    },
                    product.name
                ),
                html.div(
                    {
                        "class": "flex items-center mb-4"
                    },
                    html.span(
                        {
                            "class": "text-yellow-500 mr-1 text-xl"
                        },
                        "★" * int(product.rating)
                    ),
                    html.span(
                        {
                            "class": "text-gray-400 text-xl"
                        },
                        "★" * (5 - int(product.rating))
                    ),
                    html.span(
                        {
                            "class": "text-gray-600 ml-2"
                        },
                        f"({product.rating})"
                    )
                ),
                html.p(
                    {
                        "class": "text-2xl font-bold text-blue-600 mb-4"
                    },
                    f"R$ {product.price:.2f}"
                ),
                html.p(
                    {
                        "class": "text-gray-700 mb-6"
                    },
                    product.description
                ),
                html.div(
                    {
                        "class": "flex items-center mb-6"
                    },
                    html.span(
                        {
                            "class": "text-gray-600 mr-4"
                        },
                        f"Estoque: {product.stock}"
                    ),
                    html.span(
                        {
                            "class": "px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                        },
                        "Disponível" if product.stock > 0 else "Esgotado"
                    )
                ),
                html.button(
                    {
                        "class": "bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400",
                        "on_click": handle_add_to_cart,
                        "disabled": product.stock <= 0
                    },
                    "Adicionar ao Carrinho" if product.stock > 0 else "Produto Esgotado"
                )
            )
        )
    )

# ========== MAIN APP ==========

@component
def App():
    # Initialize controllers
    product_controller = ProductController()
    cart_controller = CartController()
    user_session = UserSession()
    
    # Load sample data
    product_controller.load_products(get_sample_products())
    user_session.login(get_sample_user())
    
    # State hooks
    show_cart, set_show_cart = hooks.use_state(False)
    current_page, set_current_page = hooks.use_state("home")
    selected_product_id, set_selected_product_id = hooks.use_state(None)
    
    # Render appropriate page based on state
    def render_page():
        if current_page == "home":
            return HomePage(product_controller, cart_controller)
        elif current_page == "product_detail" and selected_product_id:
            return ProductDetailPage(selected_product_id, product_controller, cart_controller)
        else:
            return HomePage(product_controller, cart_controller)
    
    return html.div(
        {
            "class": "min-h-screen bg-gray-100"
        },
        Header(cart_controller, user_session, set_show_cart, set_current_page),
        html.main(
            {
                "class": "container mx-auto py-6"
            },
            render_page()
        ),
        CartSidebar(show_cart, set_show_cart, cart_controller),
        # Overlay when cart is open
        html.div(
            {
                "class": f"fixed inset-0 bg-black bg-opacity-50 z-10 {'block' if show_cart else 'hidden'}",
                "on_click": lambda event: set_show_cart(False)
            }
        )
    )

# Run the application
if __name__ == "__main__":
    run(App)