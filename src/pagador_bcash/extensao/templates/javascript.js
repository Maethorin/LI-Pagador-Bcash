//{% load filters %}
var url = '';
var $counter = null;
var segundos = 5;
var dados = null;

function post() {
    var $form = $("#enviarPagamento");
    for (var chave in dados) {
        $form.append('<input type="hidden" name="' + chave + '" value="' + dados[chave] + '" />');
    }
    $form.submit();
}

$(function() {
    var $bcashMensagem = $(".bcash-mensagem");

    function iniciaContador() {
        $counter = $bcashMensagem.find(".segundos");
        setInterval('if (segundos > 0) { $counter.text(--segundos); }', 1000);
    }

    function enviaPagamento() {
        $bcashMensagem.find(".msg-danger").hide();
        $bcashMensagem.find(".msg-success").hide();
        $bcashMensagem.find(".msg-warning").show();
        $bcashMensagem.removeClass("alert-message-success");
        $bcashMensagem.removeClass("alert-message-danger");
        $bcashMensagem.addClass("alert-message-warning");
        var url_pagar = '{% url_loja "checkout_pagador" pedido.numero pagamento.id %}?next_url=' + window.location.href.split("?")[0];
        $.getJSON(url_pagar)
            .fail(function (data) {
                exibeMensagemErro(data.status, data.content);
            })
            .done(function (data) {
                if (data.sucesso) {
                    $("#aguarde").hide();
                    $("#redirecting").show();
                    dados = data.content.dados;
                    console.log(dados);
                    iniciaContador();
                    setTimeout('post();', 5000);
                }
                else {
                    if (data.status == 400 || data.status == 401) {
                        console.log(data.content.mensagem);
                        exibeMensagemErro(data.status, "Ocorreu um erro ao enviar os dados para o Bcash. Por favor, tente de novo");
                    }
                    else {
                        exibeMensagemErro(data.status, data.content);
                    }
                }
            });
    }

    $(".msg-danger").on("click", ".pagar", function() {
        enviaPagamento();
    });

    $(".msg-success").on("click", ".ir-mp", function() {
        post();
    });

    function exibeMensagemErro(status, mensagem) {
        $bcashMensagem.find(".msg-warning").hide();
        $bcashMensagem.toggleClass("alert-message-warning alert-message-danger");
        var $errorMessage = $("#errorMessage");
        $errorMessage.text(status + ": " + mensagem);
        $bcashMensagem.find(".msg-danger").show();
    }

    function exibeMensagemSucesso(situacao) {
        $bcashMensagem.find(".msg-warning").hide();
        $bcashMensagem.toggleClass("alert-message-warning alert-message-success");
        var $success = $bcashMensagem.find(".msg-success");
        $success.find("#redirecting").hide();
        if (situacao == "pago") {
            $success.find("#successMessage").show();
        }
        else {
            $success.find("#pendingMessage").show();
        }
        $success.show();
    }

    var pedidoPago = '{{ pedido.situacao_id }}' == '4';
    var pedidoAguardandoPagamento = '{{ pedido.situacao_id }}' == '2';

    if (window.location.search != "" && window.location.search.indexOf("failure") > -1) {
        exibeMensagemErro(500, "Pagamento cancelado no Bcash!");
    }
    else if (window.location.search != "" && window.location.search.indexOf("success") > -1 || pedidoPago) {
        exibeMensagemSucesso("pago");
    }
    else if (window.location.search != "" && window.location.search.indexOf("pending") > -1 || pedidoAguardandoPagamento) {
        exibeMensagemSucesso("aguardando");
    }
    else {
        enviaPagamento();
    }
});
