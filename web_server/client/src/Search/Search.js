import React, { Component } from 'react';
import './Search.css';
import wallimage from '../images/chicago.jpg';
import {loadImage} from '../js/main';

class Profile extends Component {
  constructor(props){
    super(props);
    this.css = document.createElement('style');
    this.css.type = 'text/css';
    this.css.innerHTML = ` body {  
      background-color: #00bcf1;
      background-image: linear-gradient(to bottom right, #00bcf1, #180CAC);
    }`;
    document.body.appendChild(this.css);
    this.wallcss = document.createElement('style');
    this.wallcss.type = 'text/css';
    this.wallcss.innerHTML = ` .wallpaper {
                        background-image: url(${wallimage});
                    }`;
    document.body.appendChild(this.wallcss);
  }

  componentDidMount(){
    loadImage('search-wallpaper');
  }

  componentWillUnmount(){
    document.body.removeChild(this.css);
    document.body.removeChild(this.wallcss);
  }

  componentWillMount() {
    this.setState({ profile: {} });
    const { userProfile, getProfile } = this.props.auth;
    if (!userProfile) {
      getProfile((err, profile) => {
        this.setState({ profile });
      });
    } else {
      this.setState({ profile: userProfile });
    }
  }
  render() {
    const { profile } = this.state;
    return (
    <div>
      <div className="wallpaper" id="search-wallpaper" data-image={wallimage}></div>
      <div className="container">
        <div className="profile-area">
          <h1>{profile.name}</h1>
          <div>
            <img src={profile.picture} alt="profile" />
            <div>
              <h3> Nickname</h3>
              <h3>{profile.nickname}</h3>
            </div>
            <pre>{JSON.stringify(profile, null, 2)}</pre>
          </div>
        </div>
      </div>
    </div>
    );
  }
}

export default Profile;
