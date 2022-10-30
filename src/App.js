import './App.css';
import React, { } from 'react';
import SidePanel from './components/SidePanel';
import { Grid } from '@mui/material';
import { Box } from '@mui/system';
import LeftSidePanel from './components/LeftSidePanel';
import Canvas from './components/Canvas';
import SettingContext from './context/SettingContext';
import ResponsiveAppBar from './components/Header';


function App() {


  React.useEffect(()=>{
    console.error("MAIN APP RENDER")
  })

  const [settings, setSettings] = React.useState({
    workingImageData:{file: '',data:''},
    boxesData:[],
    workingMode: 0
  })

  const updateSetting = (obj) => {
    // console.log("updating settings", obj);
    setSettings((old) => {
      // console.log(old, obj);
      return { ...old, ...obj };
    });
  };

  return (
    <Box className='App' >
      <SettingContext.Provider
        value={{
          settings: settings,
          updateSetting: updateSetting
        }}>
        <Grid container spacing={1}>
          <Grid item xs={12}>
            <ResponsiveAppBar /> 
          </Grid>
          <Grid item xs={1} sx={{ maxHeight: '90vh' }}>
            <LeftSidePanel />
          </Grid>
          <Grid item xs={8}>
            <Canvas />
          </Grid>

          <Grid item xs={3} >
            <SidePanel />
          </Grid>

        </Grid>
      </SettingContext.Provider>
    </Box>

  );
}

export default App;
