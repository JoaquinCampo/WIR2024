import React, { useState, useEffect } from 'react';
import { Box } from '@chakra-ui/react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function Stat(props) {
  const [datos, setDatos] = useState({});
  const [estadisticas, setEstadisticas] = useState([]);
  const [maxPuntaje, setMaxPuntaje] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!props.type) {
          const response = await fetch(`http://127.0.0.1:8000/politician/${props.name}`);
          const data = await response.json();
          setDatos(data);
          const newEstadisticas = data.stats.map(stat => stat.Reputation * 100);
          setEstadisticas(newEstadisticas);
          setMaxPuntaje(Math.max(...newEstadisticas) * 1.2);
        } else {
          setDatos({ Politician: props.name.toString() });
          setEstadisticas(props.response);
          setMaxPuntaje(Math.max(...props.response) * 1.2);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchData();
  }, [props.name, props.type, props.response]);

  let labels = [];
  if (!props.type) {
    for (let i = -7; i < 0; i++) labels.push(i);
    labels.push('Hoy');
  } else {
    for (let i = -23; i <= 0; i++) labels.push(i);
    labels.push('Ahora');
  }

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

  return (
    <Box width="40vw">
      <Line data={data} options={{plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Evaluación de la reputación'
      },
    },}} />
    </Box>
  );
}

export default Stat;
