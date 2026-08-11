import { useState } from "react";
import fondoLogin from "./assets/fondo-login.jpeg";
import "./App.css";

function App() {
  const [correo, setCorreo] = useState("");
  const [contrasenia, setContrasenia] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [usuario, setUsuario] = useState(null);
  const [modulo, setModulo] = useState("inicio");
  const [expedientes, setExpedientes] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [busqueda, setBusqueda] = useState({
    radicado: "",
    documento: "",
    nombre: "",
    codigo: ""
  });
  const [nuevoCliente, setNuevoCliente] = useState({
    tipodocumento: "",
    numdocumento: "",
    nombres: "",
    apellidos: "",
    telefono: "",
    correo: "",
    direccion: ""
  });

  const [nuevoExpediente, setNuevoExpediente] = useState({
    codigointerno: "",
    numeroradicado: "",
    asunto: "",
    descripcion: "",
    estado: "Activo",
    fechaapertura: "",
    fechacierre: "",
    idcliente: "",
    idespecialidad: ""
  });
  const [especialidades, setEspecialidades] = useState([]);
  const [mensajeExpediente, setMensajeExpediente] = useState("");

  const [mensajeCliente, setMensajeCliente] = useState("");

  const [resultados, setResultados] = useState([]);

  const iniciarSesion = async (e) => {
    e.preventDefault();
    setMensaje("");

    try {
      const respuesta = await fetch("https://sistemajuridico.onrender.com/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          correo: correo,
          contrasenia: contrasenia,
        }),
      });

      const datos = await respuesta.json();

      console.log("RESPUESTA DEL LOGIN:", datos);

      if (!respuesta.ok) {
        setMensaje(datos.detail || "Correo o contraseña incorrectos");
        return;
      }

      setUsuario(datos);

    } catch (error) {
      setMensaje("No se pudo conectar con el servidor");
      console.error(error);
    }
  };

  const cargarExpedientes = async () => {
    try {
      const [respuestaExpedientes, respuestaClientes, respuestaEspecialidades] =
        await Promise.all([
          fetch("https://sistemajuridico.onrender.com/expedientes/"),
          fetch("https://sistemajuridico.onrender.com/clientes/"),
          fetch("https://sistemajuridico.onrender.com/especialidades/")
        ]);

      const datosExpedientes = await respuestaExpedientes.json();
      const datosClientes = await respuestaClientes.json();
      const datosEspecialidades = await respuestaEspecialidades.json();

      if (!respuestaExpedientes.ok) {
        alert("No se pudieron cargar los expedientes");
        return;
      }

      setExpedientes(datosExpedientes);

      if (respuestaClientes.ok) {
        setClientes(datosClientes);
      }

      if (respuestaEspecialidades.ok) {
        setEspecialidades(datosEspecialidades);
      }

      setModulo("expedientes");

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const registrarExpediente = async (e) => {
    e.preventDefault();
    setMensajeExpediente("");

    try {
      const respuesta = await fetch(
        "https://sistemajuridico.onrender.com/expedientes/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            ...nuevoExpediente,
            idcliente: Number(nuevoExpediente.idcliente),
            idespecialidad: Number(nuevoExpediente.idespecialidad),
            fechacierre: nuevoExpediente.fechacierre || null
          })
        }
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        setMensajeExpediente(
          datos.detail || "No se pudo registrar el expediente"
        );
        return;
      }

      setMensajeExpediente(
        "Expediente registrado correctamente"
      );

      setNuevoExpediente({
        codigointerno: "",
        numeroradicado: "",
        asunto: "",
        descripcion: "",
        estado: "Activo",
        fechaapertura: "",
        fechacierre: "",
        idcliente: "",
        idespecialidad: ""
      });

      cargarExpedientes();

    } catch (error) {
      console.error(error);
      setMensajeExpediente("Error al conectar con la API");
    }
  };

  const eliminarExpediente = async (idexpediente) => {
    const confirmar = window.confirm(
      `¿Está seguro de que desea eliminar el expediente ${idexpediente}?`
    );

    if (!confirmar) {
      return;
    }

    try {
      const respuesta = await fetch(
        `https://sistemajuridico.onrender.com/expedientes/${idexpediente}`,
        {
          method: "DELETE"
        }
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        alert(datos.detail || "No se pudo eliminar el expediente");
        return;
      }

      alert("Expediente eliminado correctamente");

      cargarExpedientes();

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const cargarClientes = async () => {
    try {
      const respuesta = await fetch(
        "https://sistemajuridico.onrender.com/clientes/"
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        alert("No se pudieron cargar los clientes");
        return;
      }

      setClientes(datos);
      setModulo("clientes");

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const registrarCliente = async (e) => {
    e.preventDefault();
    setMensajeCliente("");

    try {
      const respuesta = await fetch(
        "https://sistemajuridico.onrender.com/clientes/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(nuevoCliente)
        }
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        setMensajeCliente(
          datos.detail || "No se pudo registrar el cliente"
        );
        return;
      }

      setMensajeCliente(
        `Cliente ${datos.nombres} ${datos.apellidos} registrado correctamente`
      );

      setNuevoCliente({
        tipodocumento: "",
        numdocumento: "",
        nombres: "",
        apellidos: "",
        telefono: "",
        correo: "",
        direccion: ""
      });

      cargarClientes();

    } catch (error) {
      console.error(error);
      setMensajeCliente("Error al conectar con la API");
    }
  };

  const eliminarCliente = async (idcliente) => {
    const confirmar = window.confirm(
      `¿Está seguro de que desea eliminar el cliente ${idcliente}?`
    );

    if (!confirmar) {
      return;
    }

    try {
      const respuesta = await fetch(
        `https://sistemajuridico.onrender.com/clientes/${idcliente}`,
        {
          method: "DELETE"
        }
      );

      if (!respuesta.ok) {
        const error = await respuesta.json();
        alert(error.detail || "No se pudo eliminar el cliente");
        return;
      }

      alert("Cliente eliminado correctamente");

      cargarClientes();

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const buscarExpedientes = async () => {
    try {
      const parametros = new URLSearchParams();

      if (busqueda.radicado) {
        parametros.append("radicado", busqueda.radicado);
      }

      if (busqueda.documento) {
        parametros.append("documento", busqueda.documento);
      }

      if (busqueda.nombre) {
        parametros.append("nombre", busqueda.nombre);
      }

      if (busqueda.codigo) {
        parametros.append("codigo", busqueda.codigo);
      }

      const respuesta = await fetch(
        `https://sistemajuridico.onrender.com/expedientes/buscar?${parametros.toString()}`
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        alert("No se pudo realizar la consulta");
        return;
      }

      setResultados(datos);

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const cerrarSesion = () => {
    setUsuario(null);
    setCorreo("");
    setContrasenia("");
    setModulo("inicio");
    setExpedientes([]);
  };

  // PÁGINA PRINCIPAL
  if (usuario && modulo === "inicio") {
    return (
      <div className="panel-container">

        <header className="panel-header">
          <div>
            <h1>Sistema Jurídico</h1>
            <p>
              Bienvenido, {usuario.nombres} {usuario.apellidos}
            </p>
          </div>

          <button
            className="cerrar-btn"
            onClick={cerrarSesion}
          >
            Cerrar sesión
          </button>
        </header>

        <main className="panel-main">

          <h2>Seleccione el módulo que desea utilizar</h2>

          <div className="modulos-grid">

            <div
              className="modulo-card"
              onClick={() => setModulo("consultas")}
            >
              <div className="modulo-icono">🔎</div>
              <h3>Consultas</h3>
              <p>
                Buscar expedientes por diferentes criterios
              </p>
            </div>

            <div
              className="modulo-card"
              onClick={cargarExpedientes}
            >
              <div className="modulo-icono">📁</div>
              <h3>Expedientes</h3>
              <p>
                Consultar y gestionar expedientes jurídicos
              </p>
            </div>

            <div
              className="modulo-card"
              onClick={cargarClientes}
            >
              <div className="modulo-icono">👤</div>
              <h3>Clientes</h3>
              <p>
                Consultar y gestionar información de clientes
              </p>
            </div>

          </div>

        </main>
      </div>
    );
  }

  // MÓDULO CLIENTES
  if (usuario && modulo === "clientes") {
    return (
      <div className="panel-container">

        <header className="panel-header">
          <div>
            <h1>Sistema Jurídico</h1>
            <p>Gestión de clientes</p>
          </div>

          <button
            className="cerrar-btn"
            onClick={cerrarSesion}
          >
            Cerrar sesión
          </button>
        </header>

        <main className="panel-main">

          <button
            className="volver-btn"
            onClick={() => setModulo("inicio")}
          >
            ← Volver al inicio
          </button>

          <h2>Clientes</h2>

          <p className="subtitulo">
            Registrar y consultar clientes
          </p>

          <div className="cliente-form-container">

            <h3>Añadir nuevo cliente</h3>

            <form onSubmit={registrarCliente}>

              <div className="cliente-form-grid">

                <div>
                  <label>Tipo de documento</label>

                  <select
                    value={nuevoCliente.tipodocumento}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        tipodocumento: e.target.value
                      })
                    }
                    required
                  >
                    <option value="">
                      Seleccione
                    </option>
                    <option value="CC">
                      CC
                    </option>
                    <option value="CE">
                      CE
                    </option>
                    <option value="TI">
                      TI
                    </option>
                    <option value="NIT">
                      NIT
                    </option>
                  </select>
                </div>

                <div>
                  <label>Número de documento</label>

                  <input
                    type="text"
                    value={nuevoCliente.numdocumento}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        numdocumento: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Nombres</label>

                  <input
                    type="text"
                    value={nuevoCliente.nombres}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        nombres: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Apellidos</label>

                  <input
                    type="text"
                    value={nuevoCliente.apellidos}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        apellidos: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Teléfono</label>

                  <input
                    type="text"
                    value={nuevoCliente.telefono}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        telefono: e.target.value
                      })
                    }
                  />
                </div>

                <div>
                  <label>Correo</label>

                  <input
                    type="email"
                    value={nuevoCliente.correo}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        correo: e.target.value
                      })
                    }
                  />
                </div>

                <div className="campo-completo">
                  <label>Dirección</label>

                  <input
                    type="text"
                    value={nuevoCliente.direccion}
                    onChange={(e) =>
                      setNuevoCliente({
                        ...nuevoCliente,
                        direccion: e.target.value
                      })
                    }
                  />
                </div>

              </div>

              <button
                type="submit"
                className="registrar-btn"
              >
                Registrar cliente
              </button>

            </form>

            {mensajeCliente && (
              <p className="mensaje-cliente">
                {mensajeCliente}
              </p>
            )}

          </div>

          <h3 className="resultados-titulo">
            Clientes registrados
          </h3>

          <div className="tabla-container">

            <table>

              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tipo documento</th>
                  <th>Número documento</th>
                  <th>Nombres</th>
                  <th>Apellidos</th>
                  <th>Teléfono</th>
                  <th>Correo</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>

                {clientes.map((cliente) => (
                  <tr key={cliente.idcliente}>
                    <td>{cliente.idcliente}</td>
                    <td>{cliente.tipodocumento}</td>
                    <td>{cliente.numdocumento}</td>
                    <td>{cliente.nombres}</td>
                    <td>{cliente.apellidos}</td>
                    <td>{cliente.telefono}</td>
                    <td>{cliente.correo}</td>
                    <td>
                      <button
                        type="button"
                        className="eliminar-btn"
                        onClick={() => eliminarCliente(cliente.idcliente)}
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}

              </tbody>

            </table>

          </div>

        </main>
      </div>
    );
  }

  // MÓDULO CONSULTAS
  if (usuario && modulo === "consultas") {
    return (
      <div className="panel-container">

        <header className="panel-header">
          <div>
            <h1>Sistema Jurídico</h1>
            <p>Consultas de expedientes</p>
          </div>

          <button
            className="cerrar-btn"
            onClick={cerrarSesion}
          >
            Cerrar sesión
          </button>
        </header>

        <main className="panel-main">

          <button
            className="volver-btn"
            onClick={() => setModulo("inicio")}
          >
            ← Volver al inicio
          </button>

          <h2>Consultas</h2>

          <p className="subtitulo">
            Busque expedientes por diferentes criterios
          </p>

          <div className="consulta-form">

            <div className="campo-consulta">
              <label>Número de radicado</label>
              <input
                type="text"
                placeholder="Ej: 2026-000123"
                value={busqueda.radicado}
                onChange={(e) =>
                  setBusqueda({
                    ...busqueda,
                    radicado: e.target.value
                  })
                }
              />
            </div>

            <div className="campo-consulta">
              <label>Documento del cliente</label>
              <input
                type="text"
                placeholder="Ej: 1001234567"
                value={busqueda.documento}
                onChange={(e) =>
                  setBusqueda({
                    ...busqueda,
                    documento: e.target.value
                  })
                }
              />
            </div>

            <div className="campo-consulta">
              <label>Nombre o apellido</label>
              <input
                type="text"
                placeholder="Ej: Pedro"
                value={busqueda.nombre}
                onChange={(e) =>
                  setBusqueda({
                    ...busqueda,
                    nombre: e.target.value
                  })
                }
              />
            </div>

            <div className="campo-consulta">
              <label>Código interno</label>
              <input
                type="text"
                placeholder="Ej: EXP-001"
                value={busqueda.codigo}
                onChange={(e) =>
                  setBusqueda({
                    ...busqueda,
                    codigo: e.target.value
                  })
                }
              />
            </div>

            <button
              className="buscar-btn"
              onClick={buscarExpedientes}
            >
              🔎 Buscar expediente
            </button>

          </div>

          <h3 className="resultados-titulo">
            Resultados
          </h3>

          {resultados.length === 0 ? (
            <p className="sin-resultados">
              No hay resultados para mostrar.
            </p>
          ) : (

            <div className="tabla-container">

              <table>

                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Código</th>
                    <th>Radicado</th>
                    <th>Asunto</th>
                    <th>Estado</th>
                    <th>Cliente</th>
                  </tr>
                </thead>

                <tbody>

                  {resultados.map((expediente) => (
                    <tr key={expediente.idexpediente}>
                      <td>{expediente.idexpediente}</td>
                      <td>{expediente.codigointerno}</td>
                      <td>{expediente.numeroradicado}</td>
                      <td>{expediente.asunto}</td>
                      <td>{expediente.estado}</td>
                      <td>{expediente.idcliente}</td>
                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          )}

        </main>
      </div>
    );
  }

  // MÓDULO EXPEDIENTES
  if (usuario && modulo === "expedientes") {
    return (
      <div className="panel-container">

        <header className="panel-header">
          <div>
            <h1>Sistema Jurídico</h1>
            <p>Gestión de expedientes</p>
          </div>

          <button
            className="cerrar-btn"
            onClick={cerrarSesion}
          >
            Cerrar sesión
          </button>
        </header>

        <main className="panel-main">

          <button
            className="volver-btn"
            onClick={() => setModulo("inicio")}
          >
            ← Volver al inicio
          </button>

          <h2>Expedientes</h2>

          <p className="subtitulo">
            Registrar y gestionar expedientes jurídicos
          </p>

          {/* FORMULARIO */}

          <div className="cliente-form-container">

            <h3>Añadir nuevo expediente</h3>

            <form onSubmit={registrarExpediente}>

              <div className="cliente-form-grid">

                <div>
                  <label>Código interno</label>

                  <input
                    type="text"
                    placeholder="Ej: EXP-001"
                    value={nuevoExpediente.codigointerno}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        codigointerno: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Número de radicado</label>

                  <input
                    type="text"
                    placeholder="Ej: 2026-000001"
                    value={nuevoExpediente.numeroradicado}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        numeroradicado: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Asunto</label>

                  <input
                    type="text"
                    placeholder="Asunto del proceso"
                    value={nuevoExpediente.asunto}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        asunto: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Estado</label>

                  <select
                    value={nuevoExpediente.estado}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        estado: e.target.value
                      })
                    }
                    required
                  >
                    <option value="Activo">Activo</option>
                    <option value="En proceso">En proceso</option>
                    <option value="Cerrado">Cerrado</option>
                    <option value="Suspendido">Suspendido</option>
                  </select>
                </div>

                <div className="campo-completo">
                  <label>Descripción</label>

                  <textarea
                    placeholder="Descripción del expediente"
                    value={nuevoExpediente.descripcion}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        descripcion: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Fecha de apertura</label>

                  <input
                    type="date"
                    value={nuevoExpediente.fechaapertura}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        fechaapertura: e.target.value
                      })
                    }
                    required
                  />
                </div>

                <div>
                  <label>Fecha de cierre</label>

                  <input
                    type="date"
                    value={nuevoExpediente.fechacierre}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        fechacierre: e.target.value
                      })
                    }
                  />
                </div>

                <div>
                  <label>Cliente</label>

                  <select
                    value={nuevoExpediente.idcliente}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        idcliente: e.target.value
                      })
                    }
                    required
                  >
                    <option value="">
                      Seleccione un cliente
                    </option>

                    {clientes.map((cliente) => (
                      <option
                        key={cliente.idcliente}
                        value={cliente.idcliente}
                      >
                        {cliente.nombres} {cliente.apellidos}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label>Especialidad</label>

                  <select
                    value={nuevoExpediente.idespecialidad}
                    onChange={(e) =>
                      setNuevoExpediente({
                        ...nuevoExpediente,
                        idespecialidad: e.target.value
                      })
                    }
                    required
                  >
                    <option value="">
                      Seleccione una especialidad
                    </option>

                    {especialidades.map((especialidad) => (
                      <option
                        key={especialidad.idespecialidad}
                        value={especialidad.idespecialidad}
                      >
                        {especialidad.nombreesp}
                      </option>
                    ))}
                  </select>
                </div>

              </div>

              <button
                type="submit"
                className="registrar-btn"
              >
                Registrar expediente
              </button>

            </form>

            {mensajeExpediente && (
              <p className="mensaje-cliente">
                {mensajeExpediente}
              </p>
            )}

          </div>

          {/* TABLA */}

          <h3 className="resultados-titulo">
            Expedientes registrados
          </h3>

          <div className="tabla-container">

            <table>

              <thead>
                <tr>
                  <th>ID</th>
                  <th>Código</th>
                  <th>Radicado</th>
                  <th>Asunto</th>
                  <th>Estado</th>
                  <th>Cliente</th>
                  <th>Especialidad</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>

                {expedientes.map((expediente) => {

                  const cliente = clientes.find(
                    (c) => c.idcliente === expediente.idcliente
                  );

                  const especialidad = especialidades.find(
                    (e) => e.idespecialidad === expediente.idespecialidad
                  );

                  return (
                    <tr key={expediente.idexpediente}>

                      <td>
                        {expediente.idexpediente}
                      </td>

                      <td>
                        {expediente.codigointerno}
                      </td>

                      <td>
                        {expediente.numeroradicado}
                      </td>

                      <td>
                        {expediente.asunto}
                      </td>

                      <td>
                        {expediente.estado}
                      </td>

                      <td>
                        {cliente
                          ? `${cliente.nombres} ${cliente.apellidos}`
                          : expediente.idcliente}
                      </td>

                      <td>
                        {especialidad
                          ? especialidad.nombreesp
                          : expediente.idespecialidad}
                      </td>

                      <td>

                        <button
                          type="button"
                          className="eliminar-btn"
                          onClick={() =>
                            eliminarExpediente(
                              expediente.idexpediente
                            )
                          }
                        >
                          🗑️
                        </button>

                      </td>

                    </tr>
                  );

                })}

              </tbody>

            </table>

          </div>

        </main>

      </div>
    );
  }

  // LOGIN
  return (
    <div
      className="login-container"
      style={{ backgroundImage: `url(${fondoLogin})` }}
    >
      <div className="login-box">

        <h1>Sistema Jurídico</h1>

        <p>Gestión del bufete jurídico</p>

        <form onSubmit={iniciarSesion}>

          <label>Correo</label>

          <input
            type="email"
            value={correo}
            onChange={(e) => setCorreo(e.target.value)}
            placeholder="Ingrese su correo"
            required
          />

          <label>Contraseña</label>

          <input
            type="password"
            value={contrasenia}
            onChange={(e) => setContrasenia(e.target.value)}
            placeholder="Ingrese su contraseña"
            required
          />

          <button type="submit">
            Iniciar sesión
          </button>

        </form>

        {mensaje && (
          <p className="mensaje">
            {mensaje}
          </p>
        )}

      </div>
    </div>
  );
}

export default App;