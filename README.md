# Sistema para el control de incidencias
Desarrollado en Django 10.6, haciendo uso de html5, css3, Javascript con Jquery, Boostrap y PostgreSQL.

Descripción del Proceso: La empresa brinda servicios de internet, telefonía y cable, ya sea para hogares o empresas. El cliente notifica cuando ocurre un problema en el servicio, y esto es registrado por el Asesor quien toma nota de los detalles y inmediatamente asigna a un Back Office que atienda este problema, una vez solucionado esto el Back Office debe tomar nota de todos los detalles.

El sistema maneja dos tipos de usuario: Asesor, quien registra y genera las incidencias notificadas por los clientes, y el Back Office que soluciona y culmina las incidencias. Ambos usuarios pueden agregar detalles a cada incidencia que no están culminadas, también pueden buscar a los cliente sea por su RUC(cuando es empresa) o DNI(cuando es servicio de hogar), y buscar las incidencias por su numero que es generado cuando el Asesor las registra. Por ultimo el sistema genera un reporte en excel mostrando detalles de las incidencias atendidas en un rango de fechas indicado solo por el Back Office.
