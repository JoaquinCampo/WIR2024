import React, { useState, useEffect } from 'react';
import { Box } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function Stat(props) {
  const [datos, setDatos] = useState([]);
  const [datosContrincante, setDatosContrincante] = useState([]);
  const [estadisticas, setEstadisticas] = useState([]);
  const [estadisticasContrincante, setEstadisticasContrincante] = useState([]);
  const [maxPuntaje, setMaxPuntaje] = useState(0);
  const [maxPuntajeContrincante, setMaxPuntajeContrincante] = useState(0);

  useEffect(() => {
    let url = 'http://127.0.0.1:8000/politician/' + props.name;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        setDatos(data);
        const newEstadisticas = data.stats.map(stat => stat.Reputation * 100);
        setEstadisticas(newEstadisticas);
        setMaxPuntaje(Math.max(...newEstadisticas) * 1.2);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, [props.name]);

  let labels = []
  for(let i = -7; i < 0; i++)
    labels.push(i)
  labels.push('Hoy');

  const data = {
    labels: labels,
    datasets: [
      {
        label: datos.Politician,
        data: estadisticas,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: false,
        text: 'Chart.js Line Chart',
      },
    },
    scales: {
      y: {
        min: 0,
        max: maxPuntaje,
      },
    },
  };

  return (
    <Box width="40vw">
      <Line data={data} options={options} />
    </Box>
  );
}

export default Stat;
