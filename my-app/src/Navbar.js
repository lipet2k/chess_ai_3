import React from 'react'
import { Navbar, NavbarToggler, NavItem, NavLink } from 'reactstrap';

class Navigation extends React.Component {
    render() {
        return (
            <div className='nav'>
                <Navbar color='dark' expand='md' dark>
                    <div className="container">
                        <a href="#" className="navbar-brand">Chess Engine</a>

                        <NavbarToggler onClick={function noRefCheck(){}} />
                        
                    </div>
                </Navbar>
            </div>
        );
    }
}

export default Navigation;