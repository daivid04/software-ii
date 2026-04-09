export function confirmDelete(productId) {
  return new Promise((resolve) => {
    const modalContainer = document.getElementById("modal-container");
    if (!modalContainer) {
      resolve(false);
      return;
    }

    modalContainer.innerHTML = `
      <div class="modal-overlay">
        <div class="modal-confirm">
          <div class="modal-header">
            <h3 class="form-title">Confirmar eliminación</h3>
          </div>
          <p id="confirm-message">¿Está seguro que desea eliminar este producto?</p>
          <div class="form-actions">
            <button type="button" class="btn-cancel">Cancelar</button>
            <button type="button" class="btn-delete confirmation-action">Eliminar</button>
          </div>
        </div>
      </div>
    `;

    document.body.style.overflow = "hidden";

    const overlay = modalContainer.querySelector(".modal-overlay");
    const btnCancel = modalContainer.querySelector(".btn-cancel");
    const btnDelete = modalContainer.querySelector(".btn-delete");

    const close = (result) => {
      modalContainer.innerHTML = "";
      document.body.style.overflow = "";
      resolve(result);
    };

    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) close(false);
    });

    const escapeHandler = (event) => {
      if(event.key === "Escape") {
        close(false);
        document.removeEventListener("keydown", escapeHandler);
      }
    }
    document.addEventListener("keydown",escapeHandler);
    btnCancel.addEventListener("click", () => close(false));
    btnDelete.addEventListener("click", () => close(true));
  });
}