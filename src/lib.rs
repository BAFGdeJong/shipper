mod ships;
mod cleaner;
mod io;

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use pythonize::pythonize;

#[pyfunction]
#[pyo3(signature = (starsector_data_folder, key_by))]
#[pyo3(text_signature = "(starsector_data_folder: str, key_by: str) -> dict[str, Any]")]
fn get_ships(py: Python, starsector_data_folder: String, key_by: String) -> PyResult<Py<PyAny>> {

    let ship_data = ships::Data::new(&starsector_data_folder, &key_by).ships;

    let python_dict_bound = pythonize(py, &ship_data)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(python_dict_bound.unbind())
}

#[pymodule]
fn shipper(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_ships, m)?)?;
    Ok(())
}
