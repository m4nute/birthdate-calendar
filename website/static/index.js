const gridOptions = {
  columnDefs: [
    { field: 'id', hide: 'true' },
    { headerName: '', maxWidth: 35, checkboxSelection : true},
    { headerName: 'First Name', field: 'first_name' },
    { headerName: 'Surname', field: 'surname' },
    { headerName: 'Birthdate', field: 'birthdate'},
    { field: 'user_id',hide: 'true' },
    ],
  defaultColDef: {
    sortable: true,
    filter: true,
    animateRows: true,
    editable: true,
    flex: 1
  },
  suppressRowClickSelection: true,
  rowSelection: 'multiple',
  pagination: true,
  paginationPageSize: 10,
  onCellValueChanged: function(data) {
    validate_update(data)
    transferUpdate(data.data);
  }
};

document.addEventListener('DOMContentLoaded', function () {
  var gridDiv = document.querySelector('#myGrid');
  var currentUser = gridDiv.getAttribute('data-user');
  new agGrid.Grid(gridDiv, gridOptions);
  fetch('/api/birthdates')
    .then(response => response.json())
    .then(data => {
      filteredData = data.filter(obj => obj.user_id == currentUser);
      filteredData = convertJSONDates(filteredData)
      gridOptions.api.setRowData(filteredData);
      gridOptions.api.setDomLayout('autoHeight');
    })
    .catch()
});

function convertJSONDates(data) {
  for (let obj in data) {
    data[obj]['birthdate'] = convert(data[obj]['birthdate'])
  }
  return data
}

function convert(str) {
  var event = new Date(str);
  let date = JSON.stringify(event)
  return date.slice(1,11)
}

function selectAll() {
  return gridOptions.api.selectAll()
}
function deselectAll() {
  const selectedRows = gridOptions.api.getSelectedRows();
  if (selectedRows.length == 0)
    alert('Select birthdates before trying to deselect them!')
  else 
    return gridOptions.api.deselectAll()

}
function transferUpdate(selectedData) {
  const URL = '/update-row'
  const xhr = new XMLHttpRequest();
  sender = JSON.stringify(selectedData)
  xhr.open('POST', URL);
  xhr.send(sender);
}

function validate_update(data) {
  if (data.data['first_name'].length < 2) {
    alert('Update failed! First name must be greater than 2 characters');
    data.node.setDataValue('first_name', data.oldValue)}
  else if (data.data['surname'].length < 2) {
    alert('Update failed! Surname must be greater than 2 characters');
    data.node.setDataValue('surname', data.oldValue)}
  else if (data.data['birthdate'].length < 10) {
    alert('Update failed! Birthdate must be inserted in the correct format (yyyy-mm-dd)');
    data.node.setDataValue('birthdate', data.oldValue)}
  else {
  accepted_char = '0123456789-'
    var invalid = false
    for (var i = 0; i < data.data['birthdate'].length; i++) {
      if (!'0123456789-'.includes(data.data['birthdate'][i])){
          alert('Update failed! Birthdate field contains an invalid character')
          data.data['birthdate'] == data.oldValue
          invalid = true
          break; 
      }
    }
    if (!invalid) {
      transferUpdate(data.data)
    } 
  }
}

function getRemovedIds() {
  const selectedRows = gridOptions.api.getSelectedRows();
  selectedIds = []
  for (let i = 0; i < selectedRows.length; i++) {
    selectedIds.push(selectedRows[i].id)
  }
  return selectedIds
}
function transferRemoveIds() {
  const URL = '/delete-rows'
  const xhr = new XMLHttpRequest();
  sender = JSON.stringify(getRemovedIds())
  console.log(sender)
  xhr.open('POST', URL);
  xhr.send(sender);
}
function removeSelected() {
  const selectedData = gridOptions.api.getSelectedRows();
  if (selectedData.length == 0)
    alert('Select at least a birthdate before pressing "Remove" button!')
  else
    transferRemoveIds()
    gridOptions.api.applyTransaction({ remove: selectedData });
}