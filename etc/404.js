/**
 * Returns the version string from the URL pathname, if applicable.
 * @param {string} base - The base of the pathname, usually '/cylc-doc/'
 * @param {string} path - The pathname from the URL
 * @returns {string|undefined} version
 */
 function getVersion(base, path) {
    if (!path.startsWith(base)) {
        return;
    }
    path = path.replace(base, '');
    let pathArr = path.split('/');
    if (pathArr.length < 2 || pathArr[1] !== 'html') {
        return;
    }
    return pathArr[0];
}


/**
 * Update the HTML with the Cylc version garnered from the URL.
 * @param {string} version
 */
function setVersionInHTML(version) {
    document.getElementById('home-button')
        .setAttribute('href', `${version}/html/index.html`);
    document.querySelectorAll('.version-num').forEach((e) => {
        e.innerHTML = version;
    });
}


window.onload = () => {
    const body = document.querySelector('body');
    body.classList.remove('no-js');

    // Try and get version from URL
    const base = document.querySelector('base').getAttribute('href');
    let path = window.location.pathname;

    const version = getVersion(base, path);
    if (!version) return;

    // Check against existing versions
    fetch(`${base}versions.json`, {method: 'GET'})
        .then((response) => response.json())
        .then((versions) => {
            if (version in versions) {
                setVersionInHTML(version);
            }
        });
};
