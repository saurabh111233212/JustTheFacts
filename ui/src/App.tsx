/**
 * This is the top-level component that defines your UI application.
 *
 * This is an appropriate spot for application wide components and configuration,
 * stuff like application chrome (headers, footers, navigation, etc), routing
 * (what urls go where), etc.
 *
 * @see https://github.com/reactjs/react-router-tutorial/tree/master/lessons
 */

import React, { useState } from 'react';
import styled from 'styled-components';
import { Route, Link, Routes, useLocation } from 'react-router-dom';
import { Header, Content, Footer } from '@allenai/varnish2/components';
import {
    Toolbar,
    Box,
    List,
    IconButton,
    Drawer,
    ListItem,
    ListItemButton,
    useMediaQuery,
    useTheme,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

import { About } from './pages/About';
import { Home } from './pages/Home';
import { AppRoute } from './AppRoute';
import DisplayComp from './pages/DisplayComp';

/**
 * An array capturing the available routes in your application. You can
 * add or remove routes here.
 */
const ROUTES: AppRoute[] = [
    {
        path: '/',
        label: 'Home',
        Component: Home,
    },
    {
        path: '/about',
        label: 'About',
        Component: About,
    },
    {
        path: '/components',
        label: 'Components',
        Component: DisplayComp,
    }
];

export const App = () => {
    // Used to query the current page the user is on
    const location = useLocation();

    const theme = useTheme();
    const greaterThanMd = useMediaQuery(theme.breakpoints.up('md'));

    // Used to open and close the menu
    const [menuOpen, setMenuOpen] = useState(false);
    const handleMenuToggle = () => {
        setMenuOpen(!menuOpen);
    };


    // @ts-ignore
    const bgColor = theme.color2.N2;

    return (
        <div  style={{backgroundColor: "#E8ECF2"}}>
            <Header>
            </Header>

            <Content main>
                <Routes>
                    {ROUTES.map(({ path, Component }) => (
                        <Route key={path} path={path} element={<Component />} />
                    ))}
                </Routes>
            </Content>
            <Footer backgroundColor={bgColor}/>
        </div>
    );
};

const Menu = styled(List)`
    && {
        margin-top: ${({ theme }) => theme.spacing(3)};
    }
`;

const DrawerMenuButton = styled(ListItemButton)`
    && {
        min-width: 180px;
        max-width: 240px;
    }
`;

const SimpleLogo = styled.div`
    border-radius: 25px;
    width: 53px;
    height: 53px;
    line-height: 1;
    font-size: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    background: ${({ theme }) => theme.color.B2};
`;
