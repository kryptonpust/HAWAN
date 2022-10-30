import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import { IconButton, Tooltip } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import MouseIcon from '@mui/icons-material/Mouse';
import DeleteIcon from '@mui/icons-material/Delete';
import SettingContext from '../context/SettingContext';
import VerifiedIcon from '@mui/icons-material/Verified';

const Item = styled(Paper)(({ selected, theme }) => {
    return {

        backgroundColor: selected ? theme.palette.primary.light : '#fff',
        ...theme.typography.body2,
        padding: theme.spacing(1),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    }
});

function ColorChecker(mode, idx) {
    return mode === idx ? true : false
}

export default function LeftSidePanel(props) {
    const context = React.useContext(SettingContext)
    // const [mode, setMode] = React.useState(0)
    function handleClick(val) {
        // setMode(val)
        context.updateSetting({ workingMode: val })
    }

    return (
        <Box sx={{ width: '100%' }}>
            <Stack spacing={2}>
                <Item selected={ColorChecker(context.settings.workingMode, 0)}>
                    <IconButton onClick={() => { handleClick(0) }}>
                        <MouseIcon />
                    </IconButton>
                </Item>
                <Item selected={ColorChecker(context.settings.workingMode, 1)}>
                    <Tooltip title="Create New Region (c)">
                    <IconButton onClick={() => { handleClick(1) }}>
                        <AddIcon />
                    </IconButton>
                    </Tooltip>
                </Item>
                <Item selected={ColorChecker(context.settings.workingMode, 2)}>
                    <Tooltip title="Keep Selected (s)">
                        <IconButton onClick={() => { handleClick(2) }}>
                            <VerifiedIcon />
                        </IconButton>
                    </Tooltip>
                </Item>
                <Item selected={ColorChecker(context.settings.workingMode, 3)}>
                    <Tooltip title="Delete Selected (d)">
                    <IconButton onClick={() => { handleClick(3) }}>
                        <DeleteIcon />
                    </IconButton>
                    </Tooltip>
                </Item>



            </Stack>
        </Box>
    );
}