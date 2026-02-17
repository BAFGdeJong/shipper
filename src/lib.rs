mod ships;
mod cleaner;
mod io;

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pythonize::pythonize;
use crate::io::CSVLoad;

#[pyfunction]
#[pyo3(signature = (starsector_data_folder, key_by))]
#[pyo3(text_signature = "(starsector_data_folder: str, key_by: str) -> dict[str, Any]")]
fn get_ships(py: Python, starsector_data_folder: String, key_by: String) -> PyResult<Py<PyAny>> {

    let ship_data = ships::Data::new(&starsector_data_folder).get_ships(&key_by);

    let python_dict_bound = pythonize(py, &ship_data)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(python_dict_bound.unbind())
}

#[pyfunction]
#[pyo3(signature = (starsector_data_folder, key_by))]
#[pyo3(text_signature = "(starsector_data_folder: str, key_by: str) -> dict[str, Any]")]
fn get_ships_minimal(py: Python, starsector_data_folder: String, key_by: String) -> PyResult<Py<PyAny>> {

    let sys = ships::Data::new(&starsector_data_folder).get_ships_minimal(&key_by);

    let python_dict_bound = pythonize(py, &sys.unwrap()) // TODO unwrap not good
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(python_dict_bound.unbind())
}

#[pyfunction]
#[pyo3(signature = (starsector_data_folder, key_by))]
#[pyo3(text_signature = "(starsector_data_folder: str, key_by: str) -> dict[str, Any]")]
fn get_hull_mods(py: Python, starsector_data_folder: String, key_by: String) -> PyResult<Py<PyAny>> {
    let hull_mods = ships::Data::new(&starsector_data_folder).get_hullmods(&key_by);

    let python_dict_bound = pythonize(py, &hull_mods.unwrap()) // TODO unwrap not good
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(python_dict_bound.unbind())
}

#[pyfunction]
#[pyo3(signature = (starsector_data_folder, key_by))]
#[pyo3(text_signature = "(starsector_data_folder: str, key_by: str) -> dict[str, Any]")]
fn get_ship_systems(py: Python, starsector_data_folder: String, key_by: String) -> PyResult<Py<PyAny>> {

    let sys = ships::Data::new(&starsector_data_folder).get_ship_systems(&key_by);

    let python_dict_bound = pythonize(py, &sys.unwrap()) // TODO unwrap not good
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(python_dict_bound.unbind())
}

#[pymodule]
fn shipper(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_ships, m)?)?;
    m.add_function(wrap_pyfunction!(get_ships_minimal, m)?)?;
    m.add_function(wrap_pyfunction!(get_hull_mods, m)?)?;
    m.add_function(wrap_pyfunction!(get_ship_systems, m)?)?;
    Ok(())
}
