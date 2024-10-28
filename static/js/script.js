
        // Função para abrir o modal
        function abrirModal() {
            document.getElementById("feedbackModal").style.display = "flex";
        }

        // Função para fechar o modal
        function fecharModal() {
            document.getElementById("feedbackModal").style.display = "none";
        }

        // Simulação do fim da interação do chatbot
        setTimeout(abrirModal, 20000); // Exibe o modal após 20 segundos

        // Lógica de submissão do formulário de feedback
        document.getElementById("feedbackForm").onsubmit = async function (e) {
            e.preventDefault();
            
            const comentario = document.getElementById("comentario").value;
            const nota = document.getElementById("nota").value;

            // Envio do feedback para o backend
            const response = await fetch("/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ comentario, nota })
            });

            if (response.ok) {
                alert("Avaliação enviada com sucesso!");
                fecharModal();
            } else {
                alert("Erro ao enviar avaliação.");
            }
        };