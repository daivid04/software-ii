/** 
* @module utils/error-handlers
* @description Manejo de errores centralizados
*/

import { showNotification } from "./notification.js";

/**
 * 
 * @param {Error} error - error lanzado por la api o el sistema 
 * @param {Object} context - Contexto adicional del error (endpoint, método, datos)
 * @throws {Error} Re-lanza el error después de manejarlo
 */

export function handleApiError(error, context = {}) {
  let typeNotification = "error";
  let message = "";
  const isGraveError = error.status >= 500 || error.message?.includes("Failed to fetch");
  
  // Log básico del error (solo en desarrollo si es necesario)
  if (process.env.NODE_ENV === 'development') {
    console.error("Error capturado:", {
      error: error.message,
      status: error.status,
      endpoint: context.endpoint,
      method: context.method,
      timestamp: new Date().toISOString(),
    });
  }

  if(isGraveError) {
    // Log detallado para errores graves (solo en desarrollo)
    if (process.env.NODE_ENV === 'development') {
      console.error("Stack trace:", error.stack);
      console.error("Detalles completos:", {
        error,
        context,
        userAgent: navigator.userAgent,
      });
    }
  }
  if(error.detail) {
    showNotification(error.detail, typeNotification);
    throw error;
  }
  if (error.status) {
    switch (error.status) {
      case 200:
        message = "Proceso realizado.";
        typeNotification = "success";
        break;
      case 400:
        message = "Solicitud invalida, intente de nuevo.";
        break;
      case 401:
        message = "No autenticado, intente de nuevo.";
        break;
      case 403:
        message = "No tiene permiso para relizar esta operacion.";
        break;
      case 404:
        message = "No se encontro el recurso solicitado.";
        typeNotification = "warning";
        break;
      case 409:
        message = error.detail || "No se puede eliminar este elemento porque tiene referencias asociadas.";
        typeNotification = "warning";
        break;
      case 422:
        message = "Validacion incorrecto, intente de nuevo.";
        break;
      case 500:
        message = "Error interno del servidor, intente más tarde";
        break;
      default:
        message = "Ocurrio un error inesperado, intente de nuevo";  
        break;
      }
  } else if(error.message?.includes("Failed to fetch") || error.message.includes("NetworkError")) {
      message = "No se pudo completar la accion, compruebe su conexion a internet";
      typeNotification = "warning";
  } else {
      message = "Ocurrio un error desconocido, intente mas tarde.";
  }
  showNotification(message, typeNotification);
  throw error; 
}