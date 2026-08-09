import { useState } from "react";
import fondoLogin from "./assets/fondo-login.jpeg";

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

  const [mensajeCliente, setMensajeCliente] = useState("");

  const [resultados, setResultados] = useState([]);

  const iniciarSesion = async (e) => {
    e.preventDefault();
    setMensaje("");

    try {
      const respuesta = await fetch("http://127.0.0.1:8000/login/", {
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
      const respuesta = await fetch(
        "http://127.0.0.1:8000/expedientes/"
      );

      const datos = await respuesta.json();

      if (!respuesta.ok) {
        alert("No se pudieron cargar los expedientes");
        return;
      }

      setExpedientes(datos);
      setModulo("expedientes");

    } catch (error) {
      console.error(error);
      alert("Error al conectar con la API");
    }
  };

  const cargarClientes = async () => {
    try {
      const respuesta = await fetch(
        "http://127.0.0.1:8000/clientes/"
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
        "http://127.0.0.1:8000/clientes/",
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
        `http://127.0.0.1:8000/clientes/${idcliente}`,
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
        `http://127.0.0.1:8000/expedientes/buscar?${parametros.toString()}`
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
            Expedientes registrados en el sistema
          </p>

          <div className="tabla-container">

            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Código</th>
                  <th>Número de radicado</th>
                  <th>Asunto</th>
                  <th>Estado</th>
                  <th>Cliente</th>
                </tr>
              </thead>

              <tbody>
                {expedientes.map((expediente) => (
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

        </main>
      </div>
    );
  }

  // PANEL PRINCIPAL
  if (usuario) {
    return (
      <div className="panel-container">

        <header className="panel-header">
          <div>
            <h1>Sistema Jurídico</h1>
            <p>Gestión del bufete jurídico</p>
          </div>

          <button
            className="cerrar-btn"
            onClick={cerrarSesion}
          >
            Cerrar sesión
          </button>
        </header>

        <main className="panel-main">

          <h2>
            Bienvenido, {usuario.nombres} {usuario.apellidos}
          </h2>

          <p className="subtitulo">
            Seleccione el módulo que desea utilizar
          </p>


          <div className="modulos">
            <div className="modulos">

              <button
                className="modulo"
                onClick={() => setModulo("consultas")}
              >
                <span>🔎</span>
                <h3>Consultas</h3>
                <p>
                  Buscar expedientes por diferentes criterios
                </p>
              </button>

              <button
                className="modulo"
                onClick={cargarExpedientes}
              >
                <span>📁</span>
                <h3>Expedientes</h3>
                <p>
                  Consultar y gestionar expedientes jurídicos
                </p>
              </button>

              <button
                className="modulo"
                onClick={cargarClientes}
              >
                <span>👤</span>
                <h3>Clientes</h3>
                <p>
                  Consultar y gestionar información de clientes
                </p>
              </button>

            </div>

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