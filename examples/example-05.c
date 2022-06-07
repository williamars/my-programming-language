int sub(int a, int b) {
    int x;
    x = a - b;
    return (x);
}

str concat(str a, str b) {
    str x;
    x = a . b;
    return (x);
}

int main() {
    int a;
    int b;
    str c;
    str d;

    a = 5;
    b = 1910;

    printf(a);
    printf(b);

    c = "Essa é uma mensagem super secreta. Vc não deveria compartilhar com ninguém:";
    d = " VAI CORINTHIANS ";
    printf(sub(a, b));
    printf(concat(c, d));
    printf(d . b);
    /*
        ALGUM COMENTARIO
    */
}