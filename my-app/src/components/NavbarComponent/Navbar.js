import React from 'react';
import * as NavigationMenu from '@radix-ui/react-navigation-menu';
import classNames from 'classnames';
import { CaretDownIcon } from '@radix-ui/react-icons';
import { IoHome } from "react-icons/io5";
import "./Navbar.css"
import logo from './logo.svg';


const Navbar = () => {
    return (
      <NavigationMenu.Root className="NavigationMenuRoot">
      <NavigationMenu.List className="NavigationMenuList">
        <NavigationMenu.Item id="title-2">
          <NavigationMenu.Link className="NavigationMenuLink" href="." id="title-1">
          <img src={logo} height="30px"/><p> reviewify</p>
          </NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="NavigationMenuLink" href="https://docs.cohere.com/docs/summarize">
            Cohere
          </NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="NavigationMenuLink" href=".">
            Dashboard
          </NavigationMenu.Link>
        </NavigationMenu.Item>
        <NavigationMenu.Item>
          <NavigationMenu.Link className="NavigationMenuLink" href=".">
            <IoHome size="20px"/>
          </NavigationMenu.Link>
        </NavigationMenu.Item>

      
      </NavigationMenu.List>

      <div className="ViewportPosition">
        <NavigationMenu.Viewport className="NavigationMenuViewport" />
      </div>
    </NavigationMenu.Root>
    )
}

export default Navbar