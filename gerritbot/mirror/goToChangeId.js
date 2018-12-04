function goToChangeId(changeId) {
  if (!changeId) {
    changeId = document.getElementsByClassName('searchTextBox')[0].value.trim();
  }
  fetch('/ChangeIdToChangeNumber.json')
    .then(res => res.json())
    .then((out) => {
      console.log('Checkout this JSON! ', out);
      console.log(changeId)
      if (out.hasOwnProperty(changeId)) {
        var changeNumber = out[changeId]
        var staticUrl = window.location.origin + '/%23/c/' + changeNumber + '/';
        window.location.assign(staticUrl)
      } else {
        alert('Change-Id: ' + changeId + ' not found!')
      }
    })
    .catch(err => { throw err });
}
