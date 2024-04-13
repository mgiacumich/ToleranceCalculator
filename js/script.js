window.onload = function() {
    document.getElementById('creationDate').innerText = new Date().toLocaleDateString();
};

function computeTolerance() {
    const nominal = parseFloat(document.getElementById('nominalDiameter').value);
    const toleranceHole = parseInt(document.getElementById('typeSelect').value);
    const fitValues = document.getElementById('fitType').value.split(';');
    const clearance = fitValues.map(Number);

    const part = toleranceHole ? [0, -0.025] : [-0.025, 0];

    const tol = toleranceHole ? [
        part[1] + clearance[0],  // max hole = min shaft + max clearance
        part[0] + clearance[1]  // min hole = max shaft + min clearance
    ] : [
        part[1] - clearance[1],  // max shaft = min hole - min clearance
        part[0] - clearance[0]  // min shaft = max hole - max clearance
    ];

    const dim = [
        nominal + tol[0],
        nominal + tol[1]
    ];

    const type = toleranceHole ? 'HOLE' : 'SHAFT';
    const label = [type, 'Upper Bound', 'Lower Bound'];

    if (tol[0] < tol[1]) {
        alert('CANNOT TOLERANCE.');
        return;
    }

    document.getElementById('result').innerHTML = `
        <p>${label.join(' ')}</p>
        <p>Tolerance: Upper = ${tol[0]}, Lower = ${tol[1]}</p>
        <p>Dimension Limits: Upper = ${dim[0]}, Lower = ${dim[1]}</p>
    `;
}
